from django.urls import path
from Trending.views import TrendingView

urlpatterns = [
    path('trend-detail/',TrendingView.as_view(),name = 'trend-detail')
]
