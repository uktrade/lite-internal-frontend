from django.urls import path

from open_general_licences import views

app_name = "open_general_licences"

urlpatterns = [
    path("", views.ListView.as_view(), name="open_general_licences"),
    path("<uuid:pk>/", views.CreateView.as_view(), name="open_general_licence"),
    path("<uuid:pk>/edit/", views.UpdateView.as_view(), name="edit"),
    path("create/", views.CreateView.as_view(), name="create"),
]
