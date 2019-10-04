from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from lite_forms.components import Option
from lite_forms.generators import form_page

from cases.forms.goods_flags import flags_form
from cases.services import put_flag_assignments, get_good, get_goods_type, get_case
from flags.services import get_cases_flags, get_goods_flags


class AssignFlags(TemplateView):
    objects = None
    form = None
    selected_flags = None
    url = None
    level = None

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        kwargs = {'pk': case_id}
        self.level = request.GET.get('level')
        self.objects = request.GET.getlist('items', request.GET.getlist('goods'))
        origin = request.GET.get('origin', 'case')

        if not self.objects:
            raise Http404

        # Retrieve the list of flags depending on type
        if self.level == 'cases':
            flags = get_cases_flags(request)

        if self.level == 'goods':
            flags = get_goods_flags(request)

        # Perform pre-population of the flags if there is only one object to be flagged
        if len(self.objects) == 1:
            if self.level == 'goods':
                obj, status_code = get_good(request, self.objects[0])
                if status_code == 404:
                    obj, _ = get_goods_type(request, self.objects[0])
            elif self.level == 'cases':
                obj = {'case': get_case(request, self.objects[0])}

            # Fetches existing flags on the object
            object_flags = obj.get(self.level[:-1]).get('flags')
            self.selected_flags = {'flags': []}
            for flag in flags:
                for object_flag in object_flags:

                    # If flag is both on the object and available to the user, show that it is already set
                    if flag['id'] in object_flag['id']:
                        self.selected_flags['flags'].append(flag['id'])
                        break

            # Origin is set to tell the form where to return to after submission or when back link is clicked
            if origin == 'good':
                kwargs = {'pk': case_id, 'good_pk': self.objects[0]}
                self.url = reverse('cases:' + origin, kwargs=kwargs)
            elif origin == 'case':
                self.url = reverse('cases:' + origin, kwargs=kwargs)
            elif origin == 'review_goods':
                goods_being_edited = ""
                for pk in self.objects:
                    goods_being_edited += '?goods=' + pk
                self.url = reverse('cases:' + origin, kwargs=kwargs) + goods_being_edited
                origin = 'review good'

        flags = [Option(x['id'], x['name']) for x in flags]

        self.form = flags_form(
            flags=flags,
            level=self.level,
            origin=origin,
            url=self.url
        )

        return super(AssignFlags, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=self.selected_flags)

    def post(self, request, **kwargs):
        response, _ = put_flag_assignments(request,
                                                     {
                                                         'level': self.level,
                                                         'objects': self.objects,
                                                         'flags': request.POST.getlist('flags'),
                                                         'note': request.POST.get('note')
                                                     })

        if 'errors' in response:
            return form_page(request, self.form, data=request.POST, errors=response['errors'])

        return redirect(self.url)
