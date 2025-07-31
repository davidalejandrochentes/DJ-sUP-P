from django.urls import path
from . import views

urlpatterns = [
    path('consejos/', views.consejos, name="consejos"),
]