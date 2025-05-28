from django.urls import path
from . import views

urlpatterns = [
    path('run/<str:id>', views.run, name='run'),
    path('start', views.start, name='start'),
    path('stop', views.stop, name='stop'),
    path('save', views.save, name='save'),
    path('update_time', views.update_time, name='update_time'),
    path('time_out', views.time_out, name='time_out'),
    path('results', views.results, name='results'),
    path('result/<int:id>', views.result, name='result'),
    path('administrator', views.administrator, name='administrator'),
    path('', views.index),
]