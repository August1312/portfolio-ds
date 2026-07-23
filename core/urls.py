from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.about, name='about'),
    path('projetos/', views.projects, name='projects'),
    path('contato/', views.contact, name='contact'),
    path('analytics/', views.analytics, name='analytics'),
]

