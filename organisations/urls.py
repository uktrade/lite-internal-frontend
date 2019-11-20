from django.urls import path

from organisations import views

app_name = "organisations"

urlpatterns = [
    # ex: /organisations/
    path("", views.OrganisationList.as_view(), name="organisations"),
    path("<uuid:pk>/", views.OrganisationDetail.as_view(), name="organisation"),
    path("hmrc/", views.HMRCList.as_view(), name="hmrc"),
    # Register
    path("register/", views.RegisterBusiness.as_view(), name="register"),
    path("register-hmrc/", views.RegisterHMRC.as_view(), name="register_hmrc"),
]
