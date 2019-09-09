from django.urls import reverse_lazy
from lite_forms.components import Form, BackLink, RadioButtons, Option, TextInput, TextArea, HTMLBlock, Heading
from lite_forms.styles import HeadingStyle


def respond_to_clc_query_form(case):
    return Form(title='Respond to CLC Query',
                questions=[
                    Heading('CLC12-13279', HeadingStyle.S),
                    HTMLBlock(html='<div class="app-summary-list app-inset-text">'
                                        '<div class="app-summary-list__item">'
                                            '<p class="govuk-caption-m">Description</p>'
                                            '<p class="govuk-body-m">Lorem Ipsum</p>'
                                        '</div>'
                                        '<div class="app-summary-list__item">'
                                            '<p class="govuk-caption-m">Control Code Classification</p>'
                                            '<p class="govuk-body-m">ML1a</p>'
                                        '</div>'
                                    '</div>'),
                    HTMLBlock(html='<hr class="lite-horizontal-separator">'),
                    RadioButtons(title='Is this good controlled?',
                                 description='Example description text',
                                 name='is_good_controlled',
                                 options=[
                                     Option(key='yes',
                                            value='Yes',
                                            show_pane='pane_control_code'),
                                     Option(key='no',
                                            value='No')
                                 ],
                                 classes=['govuk-radios--inline']),
                    TextInput(title='What\'s the good\'s actual control rating?',
                              name='control_code'),
                    RadioButtons(title='Which report summary would you like to use?',
                                 description='Example description text',
                                 name='report_summary',
                                 options=[
                                     Option(key='yes',
                                            value='Annual Report Summary #1',
                                            description='I am the annual report summary text!'),
                                     Option(key='no',
                                            value='Annual Report Summary #2',
                                            description='I am the annual report summary text!'),
                                     Option(key='yes',
                                            value='Annual Report Summary #1',
                                            description='I am the annual report summary text!'),
                                     Option(key='no',
                                            value='Annual Report Summary #2',
                                            description='I am the annual report summary text!'),
                                     Option(key='yes',
                                            value='Annual Report Summary #1',
                                            description='I am the annual report summary text!'),
                                     Option(key='no',
                                            value='Annual Report Summary #2',
                                            description='I am the annual report summary text!'),
                                 ],
                                 classes=['test']),
                    TextArea(title='Why are you making this decision?',
                             description='Example text here',
                             name='comment',
                             extras={
                                 'max_length': 500,
                             }),
                ],
                back_link=BackLink('Back to case', reverse_lazy('cases:case', kwargs={'pk': case['id']})))
