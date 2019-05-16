from django.urls import path

from auth.views import AuthView, AuthCallbackView

app_name = 'authbroker_client'

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('callback/', AuthCallbackView.as_view(), name='callback'),
]
