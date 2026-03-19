from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("r/<int:room_id>/", views.room, name="room"),
    path("r/<int:room_id>/clear/", views.clear_room, name="clear_room"),
]
