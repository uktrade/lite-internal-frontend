from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls', namespace='authbroker')),
    path('', include('core.urls')),
    path('cases/', include('cases.urls')),
    path('organisations/', include('organisations.urls')),
    path('organisations/register/', include('register_business.urls')),
]
