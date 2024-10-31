from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('myapp/', views.get_resource),
    path('',views.index)
]
