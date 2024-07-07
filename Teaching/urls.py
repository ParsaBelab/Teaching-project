from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('pay/', include('prices.urls')),
    path('accounts/', include('accounts.urls')),
    path('category/',include('posts.urls')),
]
