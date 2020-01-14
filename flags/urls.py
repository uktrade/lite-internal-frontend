from django.urls import path

from flags import views

app_name = "flags"

urlpatterns = [
    path("", views.FlagsList.as_view(), name="flags"),
    # ex: /flags/assign-flags/
    # TODO - maybe remove???? let me know if you find this in the pull request!
    # path("assign-flags/", views.AssignFlags.as_view(), name="assign_flags"),
    path("<str:status>/", views.FlagsList.as_view(), name="flags"),
    path("add", views.AddFlag.as_view(), name="add"),
    path("<uuid:pk>/profile/", views.ViewFlag.as_view(), name="flag"),
    path("<uuid:pk>/edit/", views.EditFlag.as_view(), name="edit"),
    path("<uuid:pk>/edit/<str:status>/", views.ChangeFlagStatus.as_view(), name="change_status"),
]
