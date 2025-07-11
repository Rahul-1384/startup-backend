from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from cart.models import Cart
from sell_detail.models import SellDetail
from cart.seriealizers import CartSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user, is_active=True)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        try:
            book = SellDetail.objects.get(book_id=book_id)
            price_at_addition = book.book_expected_price  

            cart_item, created = Cart.objects.get_or_create(user=user, book=book, defaults={
                'quantity': quantity,
                'price_at_addition': price_at_addition
            })

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            serializer = CartSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except SellDetail.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')

        try:
            cart_item = Cart.objects.get(user=user, book__book_id=book_id, is_active=True)
            cart_item.quantity = quantity
            cart_item.save()
            serializer = CartSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Book not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user = request.user
        book_id = request.data.get('book_id')

        try:
            cart_item = Cart.objects.get(user=user, book__book_id=book_id, is_active=True)
            cart_item.delete()
            return Response({"message": "Book removed from cart"}, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Book not found in cart"}, status=status.HTTP_404_NOT_FOUND)
