from libraries.forms.components import Form, Filter, Checkboxes, BackLink, TextArea


def goods_flags_form(flags, good_or_case, url):
    return Form(
            title='Edit goods flags',
            description='',
            questions=[
                Filter(placeholder='Filter flags'),
                Checkboxes(
                    title='Select all flags that apply',
                    name='flags',
                    options=flags
                ),
                TextArea(name='note', title='Notes', description='Provide reasons for editing the flags on these goods', optional=True)
            ],
            javascript_imports=['/assets/javascripts/filter-checkbox-list.js'],
            back_link=BackLink('Back to ' + good_or_case, url))
