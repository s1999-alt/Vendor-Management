from django.urls import path
from .views import (
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    VendorPerformanceAPIView,
    MyObtainTokenPairView,
    LogoutView,
    AcknowledgePurchaseOrderAPIView,
    PurchaseOrderByVendorAPIView,
)


urlpatterns = [
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    # URLs for managing vendors
    path("vendors/", VendorListCreateAPIView.as_view(), name="vendor-list-create"),
    path(
        "vendors/<int:pk>/",
        VendorRetrieveUpdateDestroyAPIView.as_view(),
        name="vendor-retrieve-update-destroy",
    ),
    # URLs for managing purchase orders
    path(
        "purchase_orders/",
        PurchaseOrderListCreateAPIView.as_view(),
        name="purchase-order-list-create",
    ),
    path(
        "purchase_orders/<int:pk>/",
        PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(),
        name="purchase-order-retrieve-update-destroy",
    ),
    # New endpoint for listing purchase orders by vendor
    path(
        "purchase_orders/by_vendor/<int:vendor_id>/",
        PurchaseOrderByVendorAPIView.as_view(),
        name="purchase-order-by-vendor",
    ),
    # URL for retrieving vendor performance metrics
    path(
        "vendors/<int:pk>/performance/",
        VendorPerformanceAPIView.as_view(),
        name="vendor-performance",
    ),
    # URL for acknowledging purchase orders
    path(
        "purchase_orders/<int:pk>/acknowledge/",
        AcknowledgePurchaseOrderAPIView.as_view(),
        name="acknowledge-purchase-order",
    ),
]
