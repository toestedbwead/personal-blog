from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from blog.forms import RegistrationForm
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView
from django.views.generic import DetailView
from blog.models import Article

# registration view 
class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'blog/auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        user.role = 'regular_user'
        user.save()

        return super().form_valid(form)
    
# login view
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'blog/auth/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
    
# article list view | homepage
class ArticleListView(ListView):
    model = Article
    template_name = 'blog/guest/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')

# article detail view | single article
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/guest/article_detail.html'
    context_object_name = 'article'
    slug_field ='slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)