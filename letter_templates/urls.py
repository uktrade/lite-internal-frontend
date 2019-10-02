from django.urls import path

from letter_templates import views

app_name = 'letter_templates'

urlpatterns = [
    # ex: /letter-templates/
    path('', views.LetterTemplates.as_view(), name='letter_templates'),
    # ex: /letter-templates/add/
    path('add/', views.Add.as_view(), name='add'),
]
