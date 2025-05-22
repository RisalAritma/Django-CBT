from django.urls import path
from . import views

urlpatterns = [
    path('run/<str:id>', views.run, name='run'),
    path('', views.index),
]