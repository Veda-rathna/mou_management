from django.urls import path
from . import views

urlpatterns = [
    path('upload-mou/', views.upload_mou, name='upload-mou'),
    path('list-mous/', views.list_mous, name='list-mous'),
]
