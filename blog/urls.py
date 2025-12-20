from django.urls import path
from blog.views import (
    RegistrationView, LoginView, ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, UserDashboardView)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # AUTH URLs
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # GUESTS URLs
    path('articles/', ArticleListView.as_view(), name='home'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),

    # CRUD URLs
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article-edit'),
    path('articles/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete'),

    # Dashboard
    path('dashboard', UserDashboardView.as_view(), name='dashboard')
]