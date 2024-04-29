from rest_framework import serializers
from .models import Vendor , Purchase_Order


class VendorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vendor
    fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Purchase_Order
    fields = '__all__'    