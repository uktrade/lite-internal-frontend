from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from lite_forms.components import Option
from lite_forms.generators import form_page

from cases.forms.goods_flags import flags_form
from cases.services import get_flags_for_team_of_level, get_flagging_enabled_object, put_objects_flags


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
        self.objects = request.GET.getlist(self.level)
        origin = request.GET.get('origin') if request.GET.get('origin') else 'case'

        if not self.objects:
            raise Http404

        level_team_flags_data, status_code = get_flags_for_team_of_level(request, self.level)

        level_team_flags = [x for x in level_team_flags_data.get('flags') if x['status'] == 'Active']

        if len(self.objects) == 1:
            object, status_code = get_flagging_enabled_object(request, self.level, pk=self.objects[0])
            object_flags = object.get(self.level[:-1]).get('flags')
            self.selected_flags = {'flags': []}
            for flag in level_team_flags:
                for object_flag in object_flags:
                    if flag['id'] in object_flag['id']:
                        self.selected_flags['flags'].append(flag['id'])
                        break
            if origin == 'good':
                kwargs = {'pk': case_id, 'good_pk': self.objects[0]}

        flags = [Option(x['id'], x['name']) for x in level_team_flags]
        self.url = reverse('cases:' + origin, kwargs=kwargs)

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
        response, status_code = put_objects_flags(request,
                                                  {
                                                      'level': self.level,
                                                      'objects': self.objects,
                                                      'flags': request.POST.getlist('flags'),
                                                      'note': request.POST.get('note')
                                                  })

        if 'errors' in response:
            return form_page(request, self.form, data=request.POST, errors=response['errors'])

        return redirect(self.url)
