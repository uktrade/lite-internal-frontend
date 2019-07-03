from django.urls import path

from cases import views

app_name = 'cases'
urlpatterns = [
    # ex: /
    path('', views.Cases.as_view(), name='cases'),

    # ex: /<uuid:pk>/
    path('<uuid:pk>/', views.ViewCase.as_view(), name='case'),
    # ex: /<uuid:pk>/manage
    path('<uuid:pk>/manage/', views.ManageCase.as_view(), name='manage'),
    # ex: /<uuid:pk>/decide
    path('<uuid:pk>/decide/', views.DecideCase.as_view(), name='decide'),
    # ex: /<uuid:pk>/deny/
    path('<uuid:pk>/deny/', views.DenyCase.as_view(), name='deny'),
    # ex: /<uuid:pk>/move/
    path('<uuid:pk>/move/', views.MoveCase.as_view(), name='move'),
    # ex: /<uuid:pk>/attach-documents/
    path('<uuid:pk>/attach-documents/', views.AttachDocuments.as_view(), name='attach_documents'),
]
