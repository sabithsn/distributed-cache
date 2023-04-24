from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('db_query/', views.db_query, name='db_query'),
]