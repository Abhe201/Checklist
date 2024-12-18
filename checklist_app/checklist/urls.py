from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Your custom login page URL
    path('login/', views.custom_login_view, name='login'),
    
    # Checklist page
    path('', views.checklist_view, name='checklist'),

    # Django's built-in logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
