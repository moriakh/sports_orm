from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('task', views.task, name="task"),
	path('task2', views.task2, name="task2"),
	path('initialize', views.make_data, name="make_data"),
]
