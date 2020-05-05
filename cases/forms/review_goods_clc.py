from lite_content.lite_internal_frontend import goods
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.common import control_list_entries_question
from lite_forms.components import Form, BackLink, RadioButtons, Option, TextArea, DetailComponent, HelpSection

from core.services import get_control_list_entries
from lite_forms.helpers import conditional
from picklists.services import get_picklists_for_input


def review_goods_form(request, is_goods_type=True):
    return Form(
        title=cases.ReviewGoodsForm.HEADING,
        questions=[
            RadioButtons(
                title=goods.ReviewGoods.IS_GOOD_CONTROLLED,
                name="is_good_controlled",
                options=[
                    Option(
                        key=conditional(is_goods_type, True, "yes"),
                        value="Yes",
                        components=[
                            control_list_entries_question(
                                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                                title=goods.ReviewGoods.ControlListEntries.TITLE,
                            ),
                            RadioButtons(
                                title=goods.ReviewGoods.ReportSummary.TITLE,
                                name="report_summary",
                                options=get_picklists_for_input(request, "report_summary", convert_to_options=True),
                            ),
                        ],
                    ),
                    Option(key=conditional(is_goods_type, False, "no"), value="No"),
                ],
            ),
            DetailComponent(
                title="Explain why you're making this decision (optional)",
                components=[TextArea(name="comment", extras={"max_length": 500, }), ],
            ),
        ],
        default_button_name=cases.ReviewGoodsForm.CONFIRM_BUTTON,
        container="case",
        helpers=[HelpSection("Giving advice on:", "", includes="case/views/includes/advice-sidebar.html")],
    )
