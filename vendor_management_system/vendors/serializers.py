from rest_framework import serializers
from .models import Vendor , PurchaseOrder
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class VendorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vendor
    fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = PurchaseOrder
    fields = '__all__'
    extra_kwargs = {
    'po_number': {'read_only': True}}
