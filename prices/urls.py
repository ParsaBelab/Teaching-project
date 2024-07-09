from django.urls import path
from . import views

app_name = 'Prices'
urlpatterns = [
    path('price/', views.PricesView.as_view(), name='price'),
    path('start/<int:id>', views.PayStartView.as_view(), name='srart'),
    path('pay/', views.go_to_gateway_view, name='pay'),
    path('back/', views.callback_gateway_view, name='back'),

]
