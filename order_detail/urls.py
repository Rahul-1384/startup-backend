from django.urls import path
from order_detail.views import OrderListView, OrderDetailView

urlpatterns = [
    path("orders-detail/", OrderListView.as_view(), name="order-list"),
    path("orders-detail/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
