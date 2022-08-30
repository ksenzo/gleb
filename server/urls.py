from django.urls import path, re_path
from .views import game, index

urlpatterns = [
    path('', game),
    path('test', index)
]