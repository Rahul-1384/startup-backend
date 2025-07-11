from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from order_detail.models import Order
from order_detail.seriealizers import OrderSerializer

class OrderListView(APIView):
    """List all orders for an authenticated user"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve all orders for the logged-in user"""
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    """Retrieve and update order status (Admin only)"""

    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        """Retrieve order details"""
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Admin can update order status"""
        order = self.get_object(pk)
        status_choice = request.data.get("status")

        if status_choice not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_choice
        order.save()
        return Response({"message": f"Order status updated to {status_choice}"}, status=status.HTTP_200_OK)
