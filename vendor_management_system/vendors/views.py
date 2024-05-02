from rest_framework import generics
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

# View for listing and creating vendors
class VendorListCreateAPIView(generics.ListCreateAPIView):
  queryset = Vendor.objects.all()
  serializer_class = VendorSerializer


# View for retrieving, updating, and deleting vendors
class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Vendor.objects.all()
  serializer_class = VendorSerializer


# View for listing and creating purchase orders
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# View for retrieving, updating, and deleting purchase orders
class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# View for retrieving vendor performance metrics
class VendorPerformanceAPIView(generics.RetrieveAPIView):
   queryset = Vendor.objects.all()
   serializer_class = VendorSerializer
   lookup_field = 'pk'

   def get_queryset(self):
      vendor_id = self.kwargs['pk']
      vendor = Vendor.objects.get(pk=vendor_id)
      vendor.on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
      return Vendor.objects.filter(pk=vendor_id)        




