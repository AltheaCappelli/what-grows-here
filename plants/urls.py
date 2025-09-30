from django.urls import path
from . import views

urlpatterns = [
   # path('plants/', views.welcome, name='welcome_page'),
    path('plants/map/', views.map, name='map'),
    path('plants/theory/', views.theory, name='theory'),
    path('plants/about/', views.about, name='about')
    # url we want, name of view def function, name
]
