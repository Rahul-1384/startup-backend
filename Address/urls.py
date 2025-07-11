from django.urls import path
from .views import AddressListCreateView, AddressDetailView

urlpatterns = [
    path('create-get/', AddressListCreateView.as_view(), name='address-list-create'),
    path('detail/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
]