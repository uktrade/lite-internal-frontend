from django.urls import path

from picklists import views

app_name = 'picklists'
urlpatterns = [
    # ex: /picklists/ - View all active picklists
    path('', views.Picklists.as_view(), name='picklists'),
    # ex: /picklists/<uuid:pk>/ - View a picklist item
    path('<uuid:pk>/', views.PicklistItem.as_view(), name='picklist_item'),
    # ex: /picklist/add/ -  Add a new picklist item
    path('add/', views.AddPicklistItem.as_view(), name='add'),
    # # ex: /picklists/<uuid:pk>/edit/ - edit a picklist item
    path('<uuid:pk>/edit/', views.EditPicklistItem.as_view(), name='edit'),
]
