from lite_content.lite_internal_frontend import strings
from lite_forms.common import control_list_entry_question
from lite_forms.components import Form, BackLink, RadioButtons, Option, TextArea

from core.services import get_control_list_entries
from picklists.services import get_picklists


def review_goods_clc_query_form(request, back_url, is_goods_type):
    if is_goods_type:
        options = [Option(key="True", value="Yes", show_pane="pane_control_code"), Option(key="False", value="No")]
    else:
        options = [Option(key="yes", value="Yes", show_pane="pane_control_code"), Option(key="no", value="No")]

    return Form(
        title=strings.Cases.ReviewGoodsForm.HEADING,
        questions=[
            RadioButtons(
                title="Is this good controlled?",
                name="is_good_controlled",
                options=options,
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title="What is the correct control list entry?",
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Which report summary would you like to use? (optional)",
                name="report_summary",
                options=get_picklists(request, "report_summary", convert_to_options=True, include_none=True),
                description="You only need to do this if the item is controlled",
                classes=["test"],
            ),
            TextArea(title="Good's comment (optional)", name="comment", extras={"max_length": 500,}),
        ],
        default_button_name=strings.Cases.ReviewGoodsForm.CONFIRM_BUTTON,
        back_link=BackLink(strings.Cases.ReviewGoodsForm.BACK_LINK, back_url),
    )
