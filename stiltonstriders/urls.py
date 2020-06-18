from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("juniors", views.juniors, name="juniors"),
    path("seniors", views.seniors, name="seniors"),
    path("news", views.news, name="news"),
    path("events", views.events, name="events"),
    path("getEvents", views.getEvents, name="getEvents"),
    path("calendar", views.view_calendar, name="calendar"),
    path("getMonth", views.getMonth, name="getMonth"),
]