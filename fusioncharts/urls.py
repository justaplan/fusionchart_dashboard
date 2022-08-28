from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.myFirstChart , name="demo"),
   path('table', views.table_page , name="table"),
   path("people/", views.PersonListView.as_view())
]