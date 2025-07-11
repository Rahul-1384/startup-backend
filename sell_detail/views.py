from django.shortcuts import render
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sell_detail.models import SellDetail, BookPhoto,SellOrder
from sell_detail.seriealizers import SellDetailSerializer, BookPhotoSerializer,SellOrderSerializer
from order_detail.models import Order   

class SellOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all orders of the authenticated user"""
        orders = SellOrder.objects.filter(buyer=request.user)
        serializer = SellOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create an order when a user buys a book"""
        book_id = request.data.get("book_id")
        book = get_object_or_404(SellDetail, id=book_id)

        # Prevent users from buying their own book
        if book.user == request.user:
            return Response({"error": "You cannot buy your own book"}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = SellOrder.objects.create(
            buyer=request.user,
            seller=book.user,
            book=book,
            order_status="pending"
        )
        serializer = SellOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class SellDetailAPIView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
       try:
           sell_details = SellDetail.objects.all()
           serializer = SellDetailSerializer(sell_details, many=True)
           return Response(serializer.data, status=status.HTTP_200_OK)
       except Exception as e:
           return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def post(self, request):
       try:
           serializer = SellDetailSerializer(data=request.data, context={'request': request})
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e:
           return Response({"error": f"Failed to save record: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookPhotoAPIView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
       try:
           photos = BookPhoto.objects.all()
           serializer = BookPhotoSerializer(photos, many=True)
           return Response(serializer.data, status=status.HTTP_200_OK)
       except Exception as e:
           return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def post(self, request):
       try:
           serializer = BookPhotoSerializer(data=request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e:
           return Response({"error": f"Failed to save record: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PkbasedSellDetailView(APIView):
   permission_classes = [IsAuthenticated]

   def get_object(self, pk):
       return get_object_or_404(SellDetail, pk=pk, deleted_at__isnull=True)

   def get(self, request, pk):
       try:
           sell_detail = self.get_object(pk)
           serializer = SellDetailSerializer(sell_detail)
           return Response(serializer.data, status=status.HTTP_200_OK)
       except Exception as e:
           return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def put(self, request, pk):
       try:
           sell_detail = self.get_object(pk)
           serializer = SellDetailSerializer(sell_detail, data=request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_200_OK)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e:
           return Response({"error": f"Failed to update record: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def delete(self, request, pk):
       try:
           sell_detail = self.get_object(pk)
           sell_detail.deleted_at = now()  # Soft-delete the object
           sell_detail.save()
           return Response({"message": "Record successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
       except Exception as e:
           return Response({"error": f"Failed to delete record: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)