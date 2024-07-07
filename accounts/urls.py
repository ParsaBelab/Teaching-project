from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
    path('editprofile/', views.EditProfileView.as_view(), name='editprofile'),
    path('editpassword/', views.EditPasswordView.as_view(), name='editpassword'),
    path('resetpassword/', views.ResetPasswordView.as_view(), name='resetpassword'),

]
