from django.urls import path
from blog.views import RegistrationView,LoginView, ArticleListView, ArticleDetailView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # AUTH URLs
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # GUESTS URLs
    path('articles/', ArticleListView.as_view(), name='home'),
    path('articles/<slug:slug>', ArticleDetailView.as_view(), name='article-detail')
]