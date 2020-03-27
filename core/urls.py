from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("menu/", views.menu, name="menu"),
]
