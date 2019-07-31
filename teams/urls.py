from django.urls import path, include

from teams import views

app_name = 'teams'
urlpatterns = [
    # ex: /teams/
    path('', views.TeamsList.as_view(), name='teams'),
    # ex: /teams/add/
    path('add', views.AddTeam.as_view(), name='add'),
    # ex: /teams/<uuid:pk>/
    path('<uuid:pk>', views.TeamDetail.as_view(), name='team'),
    # ex: /teams/<uuid:pk>/edit/
    path('<uuid:pk>/edit', views.EditTeam.as_view(), name='edit'),
    # ex: /teams/<uuid:pk>/picklists/
    path('<uuid:pk>/picklists/', include('teams.picklists.urls')),
]
