from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), # About page
    path('contact/', views.contact, name='contact'), # Contact page
    path('upload_csv/', views.upload_csv, name='upload_csv'), # CSV file upload page
    path('terms/', views.terms, name='terms'), # Terms of service page
    path('privacy/', views.privacy, name='privacy'), # Privacy policy page
    path('generate_plot/', views.generate_plot, name='generate_plot'), # Generate plot page
]
