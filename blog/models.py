from django.db import models
from django.contrib.auth.models import AbstractUser

# category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
# user model
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('regular_user', 'Regular User')],
        default ='regular_user'
    )

# article model
class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title