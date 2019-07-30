from django.urls import path

from picklists import views

app_name = 'picklists'
urlpatterns = [
    # ex: /picklists/ - View all active picklists
    path('', views.Picklist.as_view(), name='picklists'),
    # # ex: /all/ - view all flags
    # path('<str:status>/', views.FlagsList.as_view(), name='flags'),
    # ex: /picklist/add/ -  add a new picklist item
    # path('add', views.PickListItem.as_view(), name='add'),
    # # ex: /picklist-item/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a flags's detail
    # path('<uuid:pk>/profile/', views.ViewPicklistItem.as_view(), name='picklist_item'),
    # # ex: /picklist-item/<uuid:pk>/edit - edit a picklist item
    # path('<uuid:pk>/edit/', views.EditFlag.as_view(), name='edit'),
    # # ex: /picklist-item/<uuid:pk>/edit/deactivate - deactivate or reactivate a picklist-item
    # path('<uuid:pk>/edit/<str:status>/', views.ChangePicklistItemStatus.as_view(), name='change_picklist_item_status'),
]
