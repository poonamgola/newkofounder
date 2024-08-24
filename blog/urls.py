from django.urls import path
from .views import blog, BlogSingle, category, tags

urlpatterns = [
    path('blogs/', blog, name='blogs'),
    path('category/<slug:slug>/', category, name='category'),
    path('tags/<slug:slug>/', tags, name='tags'),
    path('<slug:slug>/', BlogSingle.as_view(), name='blog_single'),
]