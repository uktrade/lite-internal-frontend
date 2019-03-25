from django.urls import path

from . import views

app_name = 'organisations'
urlpatterns = [
    path('show_orgs', views.show_orgs, name='show_orgs'),
]
