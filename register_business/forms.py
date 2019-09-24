from lite_forms.common import address_questions
from lite_forms.components import Form, TextInput, Heading, HelpSection, FormGroup, Option, RadioButtons
from lite_forms.styles import HeadingStyle
from lite_forms.helpers import conditional

from core.services import get_countries


def conditional(condition: bool, obj, obj_2=None):
    """
    Returns the object depending on a condition
    """
    if condition:
        return obj
    elif obj_2:
        return obj_2


def register_business_forms(individual=False):
    return FormGroup([
        Form(title='Commercial or private individual',
             questions=[
                 RadioButtons(name='sub_type',
                              options=[
                                  Option(key='commercial',
                                         value='Commercial'),
                                  Option(key='individual',
                                         value='Individual')
                              ])
             ]),
        conditional(individual,
                    Form(title='Register a private individual',
                         questions=[
                             TextInput(title='What\'s the individual\'s name?',
                                       name='name'),
                             TextInput(title='European Union registration and identification number (EORI)',
                                       optional=True,
                                       name='eori_number'),
                             TextInput(title='UK VAT number',
                                       description='9 digits long, with the first two letters indicating the'
                                                   ' country code of the registered business.',
                                       optional=True,
                                       name='vat_number'),
                         ],
                         default_button_name='Continue'
                         ),
                    Form(title='Register an organisation',
                         questions=[
                             TextInput(title='What\'s the organisation\'s name?',
                                       name='name'),
                             TextInput(title='European Union registration and identification number (EORI)',
                                       name='eori_number'),
                             TextInput(title='Standard Industrial Classification Number (SIC)',
                                       description='Classifies industries by a four-digit code.',
                                       name='sic_number'),
                             TextInput(title='UK VAT number',
                                       description='9 digits long, with the first two letters indicating the'
                                                   ' country code of the registered business.',
                                       name='vat_number'),
                             TextInput(title='Company registration number (CRN)',
                                       description='8 numbers, or 2 letters followed by 6 numbers.',
                                       name='registration_number'),
                         ],
                         default_button_name='Continue'
                         ),
                    ),
        Form(title='Create a default site for this exporter',
             questions=[
                 TextInput(title='Name of site',
                           name='site.name'),
                 Heading('Where is the exporter based?', HeadingStyle.M),
                 *address_questions(get_countries(None, True), 'site.address.'),
             ],
             default_button_name='Continue'),
        Form(title=conditional(individual, 'Register the individual\'s details', 'Create an admin for this organisation'),
             questions=[
                 TextInput(title='Email Address',
                           name='user.email'),
                 TextInput(title='First name',
                           name='user.first_name'),
                 TextInput(title='Last name',
                           name='user.last_name'),
             ],
             default_button_name='Submit',
             helpers=[
                 HelpSection('Help', 'This will be the default user for this organisation.')
             ]),
    ],
        show_progress_indicators=True, )
