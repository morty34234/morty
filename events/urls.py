from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('past/', views.past_events, name='past_events'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('add/', views.add_event, name='add_event'),
]