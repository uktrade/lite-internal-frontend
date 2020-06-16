from django.urls import path

import core.views
import queues.views

app_name = "core"

urlpatterns = [
    path("", queues.views.Cases.as_view(), name="index", kwargs={"disable_queue_lookup": True}),
    path("menu/", core.views.menu, name="menu"),
    path("spire-search", core.views.SpireLicenseSearch.as_view(), name="spire-search"),
]
