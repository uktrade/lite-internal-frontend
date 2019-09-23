from django.urls import path

from cases.documents import views

app_name = 'documents'
urlpatterns = [
    # ex: /flags/ - Add a document to this case
    path('create-document/', views.PickATemplate.as_view(), name='pick_a_template'),
    # ex: /flags/ - Add a document to this case
    path('create-document/generator/', views.CreateDocument.as_view(), name='create'),
    # ex: /help/ - Add a document to this case
    path('create-document/help/', views.Help.as_view(), name='help'),
]
