from django.urls import path
from cart.views import CartView

urlpatterns = [
    path('cart-detail/',CartView.as_view(),name='cart-detail')
]

