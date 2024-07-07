from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('all/', views.CategoryListView.as_view(), name='all'),
    path('<int:cat_id>/',views.CategoryDetailView.as_view(),name='detail')
]
