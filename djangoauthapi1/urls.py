from django.contrib import admin
from django.urls import path,include


admin.site.site_header = "Administration Panel"
admin.site.site_title = "My Admin"
admin.site.index_title = "Welcome to Admin Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls')),
    path('api/post-sell/', include('sell_detail.urls')),
    path('api/trends/', include('Trending.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/manga/', include('manga.urls')),
    path('api/rent/', include('rent.urls')),
    path('api/donate/', include('donate.urls')),
    path('api/order/', include('order_detail.urls')),
    path('api/address/', include('Address.urls')),
    path('api/upload-book/', include('upload_book.urls')),
]
