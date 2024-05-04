from rest_framework import generics, permissions
from .models import Vendor, PurchaseOrder
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    MyTokenObtainPairSerializer,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# Logout
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# View for listing and creating vendors
class VendorListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


# View for retrieving, updating, and deleting vendors
class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


# View for listing and creating purchase orders
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# View for retrieving, updating, and deleting purchase orders
class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# View for retrieving vendor performance metrics
class VendorPerformanceAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "pk"

    def get_queryset(self):
        vendor_id = self.kwargs["pk"]
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor.on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
        return Vendor.objects.filter(pk=vendor_id)


# View for acknowledging purchase orders
class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()
        return Response(
            {"message": "Purchase order acknowledged successfully."},
            status=status.HTTP_200_OK,
        )
