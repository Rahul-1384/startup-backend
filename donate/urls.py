from django.urls import path
from donate.views import (
    DonatedBookListCreateView,
    DonatedBookDetailView,
    DonationRequestListCreateView,
    DonationRequestDetailView,
)

urlpatterns = [
    path("create/", DonatedBookListCreateView.as_view(), name="donated-books-list"),
    path("detail/<int:pk>/", DonatedBookDetailView.as_view(), name="donated-book-detail"),
    path("requests/", DonationRequestListCreateView.as_view(), name="donation-requests"),
    path("requests/<int:pk>/", DonationRequestDetailView.as_view(), name="donation-request-detail"),
]
