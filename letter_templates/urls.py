from django.urls import path

from letter_templates import views

app_name = 'letter_templates'

urlpatterns = [
    # ex: /letter-templates/
    path('', views.LetterTemplates.as_view(), name='letter_templates'),
    # ex: /letter-templates/
    path('<uuid:pk>/', views.LetterTemplateDetail.as_view(), name='letter_template'),

    # ex: /letter-templates/add/
    path('add/', views.Add.as_view(), name='add'),
    # ex: /letter-templates/add/letter-paragraphs/
    path('add/letter-paragraphs/', views.LetterParagraphs.as_view(), name='letter_paragraphs'),
    # ex: /letter-templates/add/preview/
    path('add/preview/', views.Preview.as_view(), name='preview'),
]
