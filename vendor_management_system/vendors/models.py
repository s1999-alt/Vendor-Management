import uuid
from django.utils.timezone import now
from django.db import models
from datetime import datetime
from django.db.models import Avg, Count
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.core.exceptions import ValidationError
import re
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=10)
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    quality_rating_avg = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    average_response_time = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )
    fulfillment_rate = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    def clean(self):
        super().clean()
        if not re.match(r"^\d+$", self.contact_details):
            raise ValidationError(
                {"contact_details": "Contact details must contain exactly 10 digits."}
            )
        if not re.match(r"^[a-zA-Z\s]+$", self.name):
            raise ValidationError(
                {"name": "Name must contain only alphabetic characters and spaces."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        return super().save(*args, **kwargs)

    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status="completed")
        total_completed_pos = completed_pos.count()
        if total_completed_pos == 0:
            return 0.0
        grace_period_days = 7
        on_time_deliveries = completed_pos.filter(
            delivery_date__lte=models.F("issue_date")
            + timedelta(days=grace_period_days)
        ).count()
        return (on_time_deliveries / total_completed_pos) * 100

    def calculate_quality_rating_average(self):
        completed_pos = self.purchaseorder_set.filter(status="completed").exclude(
            quality_rating__isnull=True
        )
        if completed_pos.exists():
            return (
                completed_pos.aggregate(avg_quality_rating=Avg("quality_rating"))[
                    "avg_quality_rating"
                ]
                or 0.0
            )
        return 0.0

    def calculate_average_response_time(self):
        completed_pos = self.purchaseorder_set.filter(status="completed").exclude(
            acknowledgment_date__isnull=True
        )
        if completed_pos.exists():
            response_times = [
                (po.acknowledgment_date - po.issue_date).days for po in completed_pos
            ]
            return sum(response_times) / len(response_times)
        return 0.0

    def calculate_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.count()
        if total_pos == 0:
            return 0.0
        fulfilled_pos = self.purchaseorder_set.filter(status="completed")
        return (fulfilled_pos.count() / total_pos) * 100

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    quality_rating = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def clean(self):
        if self.order_date > self.delivery_date:
            raise ValidationError(
                {"delivery_date": "Delivery date must be after order date."}
            )

    def save(self, *args, **kwargs):
        if not self.po_number:
            unique_identifier = uuid.uuid4().hex[:10]
            date_prefix = now().strftime("%y%m%d")
            self.po_number = f"{date_prefix}-{unique_identifier}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.po_number


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.vendor_id:
        vendor = instance.vendor
        vendor.quality_rating_avg = vendor.calculate_quality_rating_average()
        vendor.average_response_time = vendor.calculate_average_response_time()
        vendor.fulfillment_rate = vendor.calculate_fulfillment_rate()
    if instance.status == "completed":
        logger.info(f"Updating on-time delivery rate for vendor {instance.vendor.id}")
        on_time_rate = vendor.calculate_on_time_delivery_rate()
        logger.info(f"On-time delivery rate: {on_time_rate}")
        vendor.on_time_delivery_rate = on_time_rate
    vendor.save()


class HistoricalPerfomance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
