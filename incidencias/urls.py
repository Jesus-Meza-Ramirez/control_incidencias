from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registrar_incidencia, name="registrar_incidencia"),
]
