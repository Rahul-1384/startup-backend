from django.urls import path
from manga.views import MangaListCreateView, MangaDetailView

urlpatterns = [
    path('create/', MangaListCreateView.as_view(), name='manga-list-create'),  # List & Create
    path('detail/<int:pk>/', MangaDetailView.as_view(), name='manga-detail'),  # Retrieve, Update, Delete
]
