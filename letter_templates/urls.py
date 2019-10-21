from django.urls import path

from letter_templates.views import manage, generator

app_name = 'letter_templates'

urlpatterns = [
    # Manage letter templates

    # ex: /<uuid:pk>/letter-templates/
    path('', manage.LetterTemplatesList.as_view(), name='letter_templates'),
    # ex: /<uuid:pk>/letter-templates/
    path('<uuid:pk>/', manage.LetterTemplateDetail.as_view(), name='letter_template'),
    # ex: /<uuid:pk>/letter-templates/edit/
    path('<uuid:pk>/edit/', manage.LetterTemplateEdit.as_view(), name='edit'),
    # ex: /<uuid:pk>/letter-templates/edit/
    path('<uuid:pk>/edit-letter-paragraphs/', manage.LetterTemplateEditLetterParagraphs.as_view(), name='edit_letter_paragraphs'),

    # Create letter templates

    # ex: /letter-templates/add/
    path('add/', generator.Add.as_view(), name='add'),
    # ex: /letter-templates/add/letter-paragraphs/
    path('add/letter-paragraphs/', generator.LetterParagraphs.as_view(), name='letter_paragraphs'),
    # ex: /letter-templates/add/preview/
    path('add/preview/', generator.Preview.as_view(), name='preview'),
]
