from django.urls import path
from .views import login_view, logout_view, dashboard_redirect

urlpatterns = [
    
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', dashboard_redirect, name='home'),
      
]
