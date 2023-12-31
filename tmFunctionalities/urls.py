from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path("createBoard/", createBoard),
    path('createCard/', createCard),
    path('createListTitle/', createListTitle),
    path('tasks/', createTask),
]
