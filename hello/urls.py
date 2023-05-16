#urls to be matched with request functions in the views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]