from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_shows, name='search'),
    path('add-to-watchlist/<int:id>/', views.add_to_watchlist, name='add-to-watchlist'),
    path('', views.watchlist, name='watchlist'),
]

