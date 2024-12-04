from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Render the frontend
    # Handle form submissions
    path('shorten/', views.shorten_url, name='shorten_url'),
    # Handle search requests
    path('search/', views.search_url, name='search_url'),
    path('<str:short_url>/', views.redirect_url,
         name='redirect_url'),  # Redirect to long URL
]
