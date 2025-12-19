from django.urls import path
from blog.views import RegistrationView,LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]