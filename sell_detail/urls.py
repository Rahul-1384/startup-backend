from django.urls import path
from sell_detail.views import SellDetailAPIView,BookPhotoAPIView,PkbasedSellDetailView

urlpatterns = [
    path('sell-detail/',SellDetailAPIView.as_view(),name='sell-detail'),
    path('book-photos/',BookPhotoAPIView.as_view(),name='book-photos'),
    path('sell-book/<str:pk>',PkbasedSellDetailView.as_view(), name = 'pk-based-sell-book-detail')
]
