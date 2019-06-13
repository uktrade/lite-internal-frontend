from django.urls import path

from teams import views

app_name = 'queues'
urlpatterns = [
    # ex: /
    path('', views.TeamsList.as_view(), name='queues'),
    # ex: /queues/add/
    path('add', views.AddTeam.as_view(), name='add'),
    # ex: /queues/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a queues's detail
    path('<uuid:pk>/', views.EditTeam.as_view(), name='edit'),
]
