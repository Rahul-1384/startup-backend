from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from donate.models import DonatedBook, DonationRequest
from donate.seriealizers import DonatedBookSerializer, DonationRequestSerializer
from order_detail.models import Order

class DonatedBookListCreateView(APIView):
    """Users & Admins can add books for donation, anyone can view"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        """List all donated books"""
        books = DonatedBook.objects.filter(is_available=True)
        serializer = DonatedBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Authenticated users & admins can donate books"""
        serializer = DonatedBookSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(donated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonatedBookDetailView(APIView):
    """Retrieve or delete a donated book"""

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(DonatedBook, pk=pk)

    def get(self, request, pk):
        """Retrieve book details"""
        book = self.get_object(pk)
        serializer = DonatedBookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Only the donor or admin can delete a book"""
        book = self.get_object(pk)
        if request.user == book.donated_by or request.user.is_staff:
            book.delete()
            return Response({"message": "Book deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)

from order_detail.models import Order  # Import Order model

class DonationRequestListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """User requests a free book"""
        serializer = DonationRequestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            donation_request = serializer.save(user=request.user)

            # Create an Order when a book is requested
            Order.objects.create(
                user=request.user,
                order_type="donate",
                donation_request=donation_request,
                status="pending"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class DonationRequestDetailView(APIView):
    """Admin can approve/reject donation requests"""

    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(DonationRequest, pk=pk)

    def patch(self, request, pk):
        """Approve or reject a request"""
        request_obj = self.get_object(pk)
        status_choice = request.data.get("status")

        if status_choice not in ["approved", "rejected"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        request_obj.status = status_choice
        request_obj.save()

        if status_choice == "approved":
            request_obj.book.is_available = False  # Mark book as taken
            request_obj.book.save()

        return Response({"message": f"Request {status_choice}"}, status=status.HTTP_200_OK)
