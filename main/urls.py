from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_course, name='search'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('tag_filter/<slug:tag>/', views.tag_search, name='tag_search'),
]
