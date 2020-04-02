from django.urls import path

from routing_rules import views

app_name = "routing_rules"

urlpatterns = [
    path("", views.RoutingRulesList.as_view(), name="list"),
    path("create/", views.CreateRoutingRule.as_view(), name="create"),
    # path("<uuid:pk>/edit/", views.EditRoutingRule.as_view(), name="edit"),
    # path("<uuid:pk>/<str:status>/", views.ChangeRoutingRuleStatus.as_view(), name="change_status"),
]
