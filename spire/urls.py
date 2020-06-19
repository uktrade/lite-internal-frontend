from django.urls import path

from spire import views


app_name = "spire"

urlpatterns = [
    path("search/", views.SpireLicenseSearch.as_view(), name="search"),
    path("licence/<str:id>/", views.SpireLicenceDetail.as_view(), name="licence"),
]
