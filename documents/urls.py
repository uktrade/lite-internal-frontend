from django.urls import path

from documents import views

app_name = 'documents'
urlpatterns = [
    # ex: /flags/ - Add a document to this case
    path('create-document/', views.CreateDocument.as_view(), name='create'),
    # ex: /flags/ - Add a document to this case
    path('create-document/2/', views.CreateDocument2.as_view(), name='create2'),
]
