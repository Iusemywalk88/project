from django.urls import path
from . import views

app_name = 'archive'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('video/<int:video_id>/', views.detail, name='detail'),
]