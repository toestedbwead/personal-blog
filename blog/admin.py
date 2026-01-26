from django.contrib import admin
from blog.models import Category, User, Article

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(User)