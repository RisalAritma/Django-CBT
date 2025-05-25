from django.urls import path
from . import views

urlpatterns = [
    path('run/<str:id>', views.run, name='run'),
    path('start', views.start, name='start'),
    path('save', views.save, name='save'),
    path('update_time', views.update_time, name='update_time'),
    path('time_out', views.time_out, name='time_out'),
    path('', views.index),
]