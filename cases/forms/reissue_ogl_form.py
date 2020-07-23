from django.urls import reverse

from lite_content.lite_internal_frontend.cases import Manage
from lite_forms.generators import confirm_form


def reissue_ogl_confirmation_form(case_id, queue_id):
    return confirm_form(
        title=Manage.ReissueOGL.TITLE,
        description=Manage.ReissueOGL.DESCRIPTION,
        confirmation_name="confirm",
        back_link_text=Manage.ReissueOGL.BACK,
        back_url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id}),
        yes_label=Manage.ReissueOGL.YES,
        no_label=Manage.ReissueOGL.NO,
        submit_button_text=Manage.ReissueOGL.SUBMIT,
        container="case",
        side_by_side=True
    )
