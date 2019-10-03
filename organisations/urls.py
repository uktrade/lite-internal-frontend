from django.urls import path

from organisations import views

app_name = 'organisations'

urlpatterns = [
    # ex: /
    path('organisations/', views.OrganisationList.as_view(), name='organisations'),
    # ex: /43a88949-5db9-4334-b0cc-044e91827451/
    path('organisations/<uuid:pk>/', views.OrganisationDetail.as_view(), name='organisation'),
    # ex: /hmrc/
    path('organisations/hmrc/', views.HMRCList.as_view(), name='hmrc')
]
