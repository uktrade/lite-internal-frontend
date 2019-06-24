from django.urls import path

from flags import views

app_name = 'flags'
urlpatterns = [
    # ex: /
    path('', views.FlagsList.as_view(), name='flags'),
    path('<str:status>/', views.FlagsList.as_view(), name='flags'),
    # ex: /queues/add/
    path('add', views.AddFlag.as_view(), name='add'),
    # ex: /queues/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a Flags's detail
    path('<uuid:pk>/profile/', views.ViewFlag.as_view(), name='flag'),
    path('<uuid:pk>/edit/', views.EditFlag.as_view(), name='edit'),
    path('<uuid:pk>/edit/<str:status>/', views.ChangeFlagStatus.as_view(), name='change_status'),
]
