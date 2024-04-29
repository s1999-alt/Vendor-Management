from rest_framework import generics
from .models import Vendor, Purchase_Order
from .serializers import VendorSerializer, PurchaseOrderSerializer


class VendorListCreateAPIView(generics.ListCreateAPIView):
  queryset = Vendor.objects.all()
  serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Vendor.objects.all()
  serializer_class = VendorSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase_Order.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceAPIView(generics.RetrieveAPIView):
   queryset = Vendor.objects.all()
   serializer_class = VendorSerializer
   lookup_field = 'pk'

   def get_queryset(self):
      vendor_id = self.kwargs['pk']
      return Vendor.objects.filter(pk=vendor_id)        




