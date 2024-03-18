from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_shows, name='search'),
    path('add-to-watchlist/<int:id>/', views.add_to_watchlist, name='add-to-watchlist'),
    path('update-show-status/<int:id>/', views.update_show_watch_status, name='update-show-status'),
    # path('profile/', views.profile, name='profile'),
    path('delete-show/<int:id>/', views.remove_from_watchlist, name='remove-from-watchlist'),
    path('', views.watchlist, name='watchlist'),
    path('show/<int:id>/', views.show_details, name='show-details'),
]

