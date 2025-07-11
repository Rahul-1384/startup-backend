from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from Trending.models import TrendingModel
from sell_detail.models import SellDetail
from Trending.seriealizers import TrendingSerializer

class TrendingView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        book_id = request.data.get('book_id')
        rank = request.data.get('rank')
        
        try:
            book = SellDetail.objects.get(id=book_id)
            trending, created = TrendingModel.objects.get_or_create(
                book=book,
                defaults={'rank': rank}
            )
            
            serializer = TrendingSerializer(trending)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except SellDetail.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        trending_books = TrendingModel.objects.all().order_by('rank')
        serializer = TrendingSerializer(trending_books, many=True)
        return Response(serializer.data)

    def delete(self, request):
        book_id = request.data.get('book_id')
        try:
            trending = TrendingModel.objects.get(book_id=book_id)
            trending.delete()
            return Response({"message": "Removed from trending"}, status=status.HTTP_200_OK)
        except TrendingModel.DoesNotExist:
            return Response({"error": "Book not in trending list"}, status=status.HTTP_404_NOT_FOUND)