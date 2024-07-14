from django.contrib import admin
from django.urls import path, include
from azbankgateways.urls import az_bank_gateways_urls
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('pay/', include('prices.urls')),
    path('accounts/', include('accounts.urls')),
    path('category/', include('posts.urls')),
    path("bankgateways/", az_bank_gateways_urls()),
)
