from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/<int:post_id>/<int:comment_id>/', views.AddReplyView.as_view(), name='reply'),
    path('toggle_favorite/<int:post_id>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
