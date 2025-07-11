from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rent.models import RentableBook, Rental
from rent.seriealizers import RentableBookSerializer, RentalSerializer
from order_detail.models import Order

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allows only admins to modify books; users can view."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

class RentableBookListCreateView(APIView):
    """List all rentable books and allow admins to add new books."""
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        search_query = request.query_params.get("search", None)
        books = RentableBook.objects.all()

        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query)
            )

        serializer = RentableBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response({"error": "Only admins can add rentable books."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RentableBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(listed_by=request.user)  # Assign admin who listed it
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RentableBookDetailView(APIView):
    """Retrieve, update, or delete a rentable book."""
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(RentableBook, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = RentableBookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Only the admin or uploader can update the book."""
        book = self.get_object(pk)

        if book.listed_by != request.user and not request.user.is_admin:
            return Response({"error": "You can only update books you listed."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RentableBookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Only the admin or uploader can delete the book."""
        book = self.get_object(pk)

        if book.listed_by != request.user and not request.user.is_admin:
            return Response({"error": "You can only delete books you listed."}, status=status.HTTP_403_FORBIDDEN)

        book.delete()
        return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

from order_detail.models import Order  # Import Order model

class RentalListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """User rents a book"""
        book_id = request.data.get("book")
        days = request.data.get("days", 1)

        if not isinstance(days, int) or days <= 0:
            return Response({"error": "Rental days must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(RentableBook, id=book_id)
        total_price = book.daily_rental_price * days
        expires_at = timezone.now() + timezone.timedelta(days=days)

        rental = Rental.objects.create(
            user=request.user,
            book=book,
            rental_days=days,
            total_price=total_price,
            expires_at=expires_at
        )

        # Create an Order when a book is rented
        Order.objects.create(
            user=request.user,
            order_type="rent",
            rental=rental,
            status="processing"
        )

        serializer = RentalSerializer(rental)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class RentalDetailView(APIView):
    """Manage an individual rental order."""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user, pk):
        return get_object_or_404(Rental, user=user, pk=pk)

    def get(self, request, pk):
        rental = self.get_object(request.user, pk)
        serializer = RentalSerializer(rental)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Users can only cancel a rental before it expires."""
        rental = self.get_object(request.user, pk)

        if rental.expires_at < timezone.now():
            return Response({"error": "You cannot delete an expired rental."}, status=status.HTTP_400_BAD_REQUEST)

        rental.delete()
        return Response({"message": "Rental canceled successfully."}, status=status.HTTP_204_NO_CONTENT)
