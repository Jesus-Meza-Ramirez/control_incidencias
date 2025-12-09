from django.urls import path
from .views import login_view, logout_view, dashboard_redirect
from . import views

urlpatterns = [
    
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', dashboard_redirect, name='home'),
    
    path('panel-admin-terminal/', views.panel_admin_terminal, name='panel_admin_terminal'),
    path('resolver-incidencia/', views.resolver_incidencia, name='resolver_incidencia'),
      
]
