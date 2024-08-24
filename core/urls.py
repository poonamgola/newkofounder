from django.urls import  path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-and-condition/', views.terms_and_condition, name='terms-and-condition'),
    path('how-it-works/', views.how_it_works, name='how-it-works'),
]