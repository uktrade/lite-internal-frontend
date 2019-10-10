from lite_forms.common import control_list_entry_question
from lite_forms.components import Form, BackLink, RadioButtons, Option, TextArea

from core.services import get_control_list_entries
from picklists.services import get_picklists


def review_goods_clc_query_form(request, back_url):
    return Form(title='Check control list classification and add report summary',
                questions=[
                    RadioButtons(title='Is this good controlled?',
                                 name='is_good_controlled',
                                 options=[
                                     Option(key='yes',
                                            value='Yes',
                                            show_pane='pane_control_code'),
                                     Option(key='no',
                                            value='No')
                                 ],
                                 classes=['govuk-radios--inline']),
                    control_list_entry_question(
                        control_list_entries=get_control_list_entries(None, convert_to_options=True),
                        title='What\'s the good\'s actual control list entry?',
                        name='control_code',
                        inset_text=False),
                    RadioButtons(title='Which report summary would you like to use?',
                                 name='report_summary',
                                 options=get_picklists(request, 'report_summary', convert_to_options=True),
                                 optional=True,
                                 description='You only need to do this if your item is controlled',
                                 classes=['test']),
                    TextArea(title='Good\'s comment',
                             name='comment',
                             optional=True,
                             extras={
                                 'max_length': 500,
                             })
                ],
                default_button_name='Add to case',
                back_link=BackLink('Back to case', back_url)
                )
