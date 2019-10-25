from django.urls import path

import letter_templates.views.edit
import letter_templates.views.letter_paragraphs
from letter_templates.views import view, create

app_name = 'letter_templates'

urlpatterns = [
    # Manage letter templates

    # ex: /<uuid:pk>/letter-templates/
    path('', view.LetterTemplatesList.as_view(), name='letter_templates'),
    # ex: /<uuid:pk>/letter-templates/
    path('<uuid:pk>/', view.LetterTemplateDetail.as_view(), name='letter_template'),
    # ex: /<uuid:pk>/letter-templates/edit/
    path('<uuid:pk>/edit/', letter_templates.views.edit.LetterTemplateEdit.as_view(), name='edit'),
    # ex: /<uuid:pk>/letter-templates/edit/
    path('<uuid:pk>/edit-letter-paragraphs/', letter_templates.views.edit.LetterTemplateEditLetterParagraphs.as_view(), name='edit_letter_paragraphs'),

    # Create letter templates

    # ex: /letter-templates/add/
    path('add/', create.Add.as_view(), name='add'),
    # ex: /letter-templates/add/letter-paragraphs/
    path('add/letter-paragraphs/', letter_templates.views.letter_paragraphs.LetterParagraphs.as_view(), name='letter_paragraphs'),
    # ex: /letter-templates/preview/
    path('preview/', create.Preview.as_view(), name='preview'),
    # ex: /letter-templates/create/
    path('create/', create.Create.as_view(), name='create'),
]
