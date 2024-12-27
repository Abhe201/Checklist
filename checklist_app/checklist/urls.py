from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import checklist_view, record_view  # Import your views

urlpatterns = [
    # Your custom login page URL
    path('login/', views.custom_login_view, name='login'),
    
    path('', checklist_view, name='checklist'),  # Checklist view for Users
    path('report/', record_view, name='records'),  # Report view for Admins

    # Django's built-in logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
