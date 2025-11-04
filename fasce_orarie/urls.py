from django.urls import path
from . import views

urlpatterns = [
    path("<str:codice_sala>/", views.fasce_orarie, name="fasce_orarie"),
]