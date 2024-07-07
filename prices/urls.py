from django.urls import path
from . import views

app_name = 'Prices'
urlpatterns = [
    path('price/', views.PricesView.as_view(), name='price')
]
