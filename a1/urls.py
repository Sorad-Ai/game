from django.contrib import admin
from django.urls import path, include
from a1 import views, hands
from .views import search_projects, appp
from . import views

urlpatterns = [
    path('', views.main),
    path('app', views.app),
    path('search/', search_projects, name='search_projects'),
    path('app/', appp, name='appp'),
    path('video_key1/', hands.video_feed, name='video_key1'),
    path('get-suggestions/', views.get_suggestions, name='get_suggestions'),

]
