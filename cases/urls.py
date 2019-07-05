from django.urls import path

from cases import views

app_name = 'cases'
urlpatterns = [
    # ex: /
    path('', views.index, name='cases'),
    # ex: /<uuid:pk>/
    path('<uuid:pk>/', views.ViewCase.as_view(), name='case'),
    # ex: clc/<uuid:pk>/
    path('clc-query/<uuid:pk>/', views.ViewCLCCase.as_view(), name='case-clc-query'),
    # ex: /<uuid:pk>/manage
    path('<uuid:pk>/manage/', views.ManageCase.as_view(), name='manage'),
    # ex: /<uuid:pk>/decide
    path('<uuid:pk>/decide/', views.DecideCase.as_view(), name='decide'),
    # ex: /<uuid:pk>/deny/
    path('<uuid:pk>/deny/', views.DenyCase.as_view(), name='deny'),
    # ex: /<uuid:pk>/move/
    path('<uuid:pk>/move/', views.MoveCase.as_view(), name='move'),
]
