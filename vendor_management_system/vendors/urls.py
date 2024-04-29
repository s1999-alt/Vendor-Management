from django.urls import path
from .views import VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView, PurchaseOrderListCreateAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView, VendorPerformanceAPIView


urlpatterns = [
  path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
  path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
  path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
  path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
  path('vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]