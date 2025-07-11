from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import UploadBook
from .seriealizers import UploadBookSerializer, AdminUploadBookSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        return obj.user == request.user


class BookListCreateAPIView(APIView):
    """
    API view for listing and creating book uploads.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request):
        """
        List books based on user role.
        Admins see all books, regular users see only their own.
        """
        user = request.user
        if user.is_staff:
            books = UploadBook.objects.all()
        else:
            books = UploadBook.objects.filter(user=user)
            
        serializer = UploadBookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new book upload.
        """
        serializer = UploadBookSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                user=request.user, 
                status=UploadBook.Status.PENDING,
                final_price=None,  
                discount=None
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """
    API view for retrieving, updating and deleting book uploads.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self, pk):
        """
        Helper method to get book object and check permissions.
        """
        book = get_object_or_404(UploadBook, pk=pk)
        self.check_object_permissions(self.request, book)
        return book
    
    def get(self, request, pk):
        """
        Retrieve a book detail.
        """
        book = self.get_object(pk)
        serializer = UploadBookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a book.
        For admins, allow updating all fields including final_price.
        For regular users, restrict updating admin-only fields.
        """
        book = self.get_object(pk)
        user = request.user
        
        if user.is_staff:
            serializer = AdminUploadBookSerializer(book, data=request.data)
        else:
            data = request.data.copy()
            for field in ['final_price', 'discount', 'status', 'admin_notes']:
                if field in data:
                    data.pop(field)
            
            serializer = UploadBookSerializer(book, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a book.
        """
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminPricingAPIView(APIView):
    """
    API view specifically for admins to set prices on book uploads.
    """
    permission_classes = [permissions.IsAdminUser]
    
    def patch(self, request, pk):
        """
        Allow admins to update just the pricing fields.
        """
        book = get_object_or_404(UploadBook, pk=pk)
        
        allowed_fields = ['final_price', 'discount', 'status', 'admin_notes']
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        serializer = AdminUploadBookSerializer(book, data=update_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingBooksAPIView(APIView):
    """
    API view for admins to get a list of books pending price approval.
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        pending_books = UploadBook.objects.filter(status=UploadBook.Status.PENDING)
        serializer = AdminUploadBookSerializer(pending_books, many=True)
        return Response(serializer.data)