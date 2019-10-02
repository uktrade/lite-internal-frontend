from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls', namespace='authbroker')),
    path('cases/', include('cases.urls')),
    path('flags/', include('flags.urls')),
    path('organisations/', include('organisations.urls')),
    path('organisations/register/', include('register_business.urls')),
    path('team/picklists/', include('picklists.urls')),
    path('team', include('teams.urls')),
    path('queues/', include('queues.urls')),
    path('users/', include('users.urls')),
    path('letter-templates/', include('letter_templates.urls'))
]
