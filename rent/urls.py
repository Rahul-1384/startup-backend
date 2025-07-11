from django.urls import path
from rent.views import (
    RentableBookListCreateView, 
    RentableBookDetailView, 
    RentalListCreateView, 
    RentalDetailView
)

urlpatterns = [
    path('create/', RentableBookListCreateView.as_view(), name='rentable-book-list-create'),
    path('detail/<int:pk>/', RentableBookDetailView.as_view(), name='rentable-book-detail'),
    path('rentals-create/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('rentals-detail/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
] 