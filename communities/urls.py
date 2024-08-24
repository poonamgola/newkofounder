from django.urls import  path
from . import views
urlpatterns = [
    path('communities/', views.Community, name='communities'),
    path('community/<slug:slug>/', views.CommunitySingle.as_view(), name='community_single'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    
]