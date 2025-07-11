# urls.py
from django.urls import path
from .views import (
    BookListCreateAPIView, 
    BookDetailAPIView, 
    AdminPricingAPIView,
    PendingBooksAPIView
)

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:pk>/pricing/', AdminPricingAPIView.as_view(), name='admin-pricing'),
    path('books/pending/', PendingBooksAPIView.as_view(), name='pending-books'),
]