from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from blog.forms import RegistrationForm, ArticleForm
from django.contrib.auth.views import LogoutView
from blog.models import Article

# AUTH VIEWS

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


# GUEST VIEWS 

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
    
# CRUD VIEWS

# create article
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/articles/article_form.html'
    success_url = reverse_lazy('dashboard')
    login_url = 'login'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# edit article
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/articles/article_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('dashboard')
    login_url = 'login'

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user
    
    def handle_no_permission(self):
        raise Http404("You don't have permission to edit this article.")
    
# delete article
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/articles/article_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('dashboard')
    login_url = 'login'

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user
    
    def handle_no_permission(self):
        raise Http404("You don't have permission to delete this article.")
    
# user dashboard
class UserDashboardView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/dashboard/dashboard.html'
    context_object_name = 'articles'
    login_url = 'login'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_articles = Article.objects.filter(author=self.request.user)
        context['total_articles'] = user_articles.count()
        context['published_articles'] = user_articles.filter(is_published=True).count()
        context['draft_articles'] = user_articles.filter(is_published=False).count()
        return context