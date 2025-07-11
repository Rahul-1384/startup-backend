from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from manga.models import Manga
from manga.seriealizers import MangaSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only admins to modify manga, users can only view."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  
            return True
        return request.user.is_authenticated and request.user.is_admin  

class MangaListCreateView(APIView):
    """List all manga (for users) and allow admins to add new manga."""

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        search_query = request.query_params.get("search", None)
        mangas = Manga.objects.all()

        if search_query:
            mangas = mangas.filter(title__icontains=search_query)

        serializer = MangaSerializer(mangas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MangaSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MangaDetailView(APIView):
    """Retrieve, update, or delete a manga entry."""

    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Manga, pk=pk)

    def get(self, request, pk):
        manga = self.get_object(pk)
        serializer = MangaSerializer(manga)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Full update - Requires all fields."""
        manga = self.get_object(pk)
        
        if manga.added_by != request.user and not request.user.is_admin:
            return Response({"error": "You can only edit your own uploads."}, status=status.HTTP_403_FORBIDDEN)

        serializer = MangaSerializer(manga, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partial update - Allows updating only selected fields."""
        manga = self.get_object(pk)
        
        if manga.added_by != request.user and not request.user.is_admin:
            return Response({"error": "You can only edit your own uploads."}, status=status.HTTP_403_FORBIDDEN)

        serializer = MangaSerializer(manga, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        manga = self.get_object(pk)

        if manga.added_by != request.user and not request.user.is_admin:
            return Response({"error": "You can only delete your own uploads."}, status=status.HTTP_403_FORBIDDEN)

        manga.delete()
        return Response({"message": "Manga deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
