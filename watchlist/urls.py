from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_shows, name='search'),
    path('add-to-watchlist/<int:id>/', views.add_to_watchlist, name='add-to-watchlist'),
    path('', views.watchlist, name='watchlist'),
]

