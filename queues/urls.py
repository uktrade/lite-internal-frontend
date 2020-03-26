from django.urls import path

from queues import views

app_name = "queues"
urlpatterns = [
    path("", main.Cases.as_view(), name="cases", kwargs={"queue_pk": ALL_CASES_QUEUE_ID}),
    path("<uuid:queue_pk>/", main.Cases.as_view(), name="cases"),

    path("manage/", views.QueuesList.as_view(), name="queues"),
    path("manage/add/", views.AddQueue.as_view(), name="add"),
    path("<uuid:pk>/", views.EditQueue.as_view(), name="edit"),
    path("<uuid:pk>/case-assignments/", views.CaseAssignments.as_view(), name="case_assignments"),
]
