from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Render the frontend
    path('shorten/', views.shorten_url, name='shorten_url'),  # Handle form submissions
    path('<str:short_url>/', views.redirect_url, name='redirect_url'),  # Redirect to long URL
]
