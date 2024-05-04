from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from vendors.models import Vendor, PurchaseOrder, HistoricalPerfomance
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from vendors.serializers import VendorSerializer
from datetime import datetime


class VendorAPITestCase(APITestCase):
    def setUp(self):
        # Get the user model
        User = get_user_model()
        # Create a superuser for testing
        User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword",
        )
        # Create a vendor for testing
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="1234567890",
            address="123 Main St",
            vendor_code="TEST123",
        )

    def get_token(self):
        serializer = TokenObtainPairSerializer(
            data={
                "username": "superuser",
                "password": "superpassword",
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["access"]

    def test_vendor_list_endpoint(self):
        # Include the JWT token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "Test Vendor")

    def test_retrieve_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-retrieve-update-destroy", kwargs={"pk": self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Test Vendor")

    def test_create_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-list-create")
        data = {
            "name": "New Vendor",
            "contact_details": "9876543210",
            "address": "456 Elm St",
            "vendor_code": "NEW123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_update_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-retrieve-update-destroy", kwargs={"pk": self.vendor.pk})
        data = {
            "name": "Updated Vendor",
            "contact_details": "9876543210",
            "address": "456 Elm St",
            "vendor_code": "TEST123",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, "Updated Vendor")

    def test_delete_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-retrieve-update-destroy", kwargs={"pk": self.vendor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(pk=self.vendor.pk).exists())

    def test_invalid_create_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-list-create")
        data = {
            "name": "Invalid Vendor",
            "contact_details": "invalid_contact_details",
            "address": "789 Oak St",
            "vendor_code": "INVALID123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_retrieve_nonexistent_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse(
            "vendor-retrieve-update-destroy", kwargs={"pk": 999}
        ) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-retrieve-update-destroy", kwargs={"pk": 999})
        data = {
            "name": "Updated Vendor",
            "contact_details": "9876543210",
            "address": "456 Elm St",
            "vendor_code": "TEST123",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_vendor_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-retrieve-update-destroy", kwargs={"pk": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword",
        )
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="1234567890",
            address="123 Main St",
            vendor_code="TEST123",
        )

        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=self.vendor,
            order_date="2024-04-30",
            delivery_date="2024-05-05",
            items={},
            quantity=10,
            status="pending",
        )

    def get_token(self):
        serializer = TokenObtainPairSerializer(
            data={
                "username": "superuser",
                "password": "superpassword",
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["access"]

    def test_list_purchase_orders_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("purchase-order-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse(
            "purchase-order-retrieve-update-destroy",
            kwargs={"pk": self.purchase_order.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["po_number"], "PO123")

    def test_create_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("purchase-order-list-create")
        data = {
            "po_number": "PO456",
            "vendor": self.vendor.pk,
            "order_date": "2024-04-30",
            "delivery_date": "2024-05-05",
            "items": {},
            "quantity": 5,
            "status": "pending",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_update_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse(
            "purchase-order-retrieve-update-destroy",
            kwargs={"pk": self.purchase_order.pk},
        )
        data = {
            "po_number": "PO123",
            "vendor": self.vendor.pk,
            "order_date": "2024-04-30",
            "delivery_date": "2024-05-05",
            "items": {},
            "quantity": 20,
            "status": "pending",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.quantity, 20)

    def test_delete_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse(
            "purchase-order-retrieve-update-destroy",
            kwargs={"pk": self.purchase_order.pk},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            PurchaseOrder.objects.filter(pk=self.purchase_order.pk).exists()
        )

    def test_invalid_create_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("purchase-order-list-create")
        data = {
            "po_number": "PO456",
            "vendor": self.vendor.pk,
            "order_date": "2024-04-30",
            "delivery_date": "2024-05-05",
            "items": {},
            "quantity": "invalid_quantity",
            "status": "pending",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PurchaseOrder.objects.count(), 1)

    def test_retrieve_nonexistent_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("purchase-order-retrieve-update-destroy", kwargs={"pk": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("purchase-order-retrieve-update-destroy", kwargs={"pk": 999})
        data = {
            "po_number": "PO999",
            "vendor": self.vendor.pk,
            "order_date": "2024-04-30",
            "delivery_date": "2024-05-05",
            "items": {},
            "quantity": 15,
            "status": "pending",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("purchase-order-retrieve-update-destroy", kwargs={"pk": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VendorPerformanceAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword",
        )
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="1234567890",
            address="123 Main St",
            vendor_code="TEST123",
        )

    def get_token(self):
        serializer = TokenObtainPairSerializer(
            data={
                "username": "superuser",
                "password": "superpassword",
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["access"]

    def test_retrieve_vendor_performance_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-performance", kwargs={"pk": self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["on_time_delivery_rate"], 0.0)

    def test_update_vendor_performance_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse("vendor-performance", kwargs={"pk": self.vendor.pk})
        data = {"on_time_delivery_rate": 80.0}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AcknowledgePurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword",
        )

        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="1234567890",
            address="123 Main St",
            vendor_code="TEST123",
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now(),
            items={},
            quantity=10,
            status="pending",
        )

    def get_token(self):
        serializer = TokenObtainPairSerializer(
            data={
                "username": "superuser",
                "password": "superpassword",
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["access"]

    def test_acknowledge_purchase_order_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_token())
        url = reverse(
            "acknowledge-purchase-order", kwargs={"pk": self.purchase_order.pk}
        )
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)

