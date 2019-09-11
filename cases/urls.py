from django.urls import path

from cases.views import main, advice, goods, flags

app_name = 'cases'
urlpatterns = [
    # ex: /cases/
    path('', main.Cases.as_view(), name='cases'),
    # ex: /cases/<uuid:pk>/
    path('<uuid:pk>/', main.ViewCase.as_view(), name='case'),
    # ex: /cases/<uuid:pk>/manage
    path('<uuid:pk>/manage/', main.ManageCase.as_view(), name='manage'),
    # ex: /cases/<uuid:pk>/decide
    path('<uuid:pk>/decide/', main.DecideCase.as_view(), name='decide'),
    # ex: /cases/<uuid:pk>/deny/
    path('<uuid:pk>/deny/', main.DenyCase.as_view(), name='deny'),
    # ex: /cases/<uuid:pk>/move/
    path('<uuid:pk>/move/', main.MoveCase.as_view(), name='move'),
    # ex: /<uuid:pk>/documents/
    path('<uuid:pk>/documents/', main.Documents.as_view(), name='documents'),
    # ex: /<uuid:pk>/documents/attach/
    path('<uuid:pk>/attach/', main.AttachDocuments.as_view(), name='attach_documents'),
    # ex: /<uuid:pk>/documents/<str:file_id>/
    path('<uuid:pk>/documents/<str:file_pk>/', main.Document.as_view(), name='document'),
    # ex: /<uuid:pk>/goods/<str:good_pk>/
    path('<uuid:pk>/goods/<str:good_pk>/', goods.Good.as_view(), name='good'),
    # ex: /cases/<uuid:pk>/assign-flags/
    path('<uuid:pk>/assign-flags/', flags.AssignFlags.as_view(), name='assign_flags'),
    # ex: /cases/<uuid:pk>/user-advice-view/
    path('<uuid:pk>/user-advice-view/', advice.ViewUserAdvice.as_view(), name='user_advice_view'),
    # ex: /cases/<uuid:pk>/team-advice-view/coalesce
    path('<uuid:pk>/team-advice-view/coalesce', advice.CoalesceUserAdvice.as_view(), name='coalesce_user_advice'),
    # ex: /cases/<uuid:pk>/team-advice-view/
    path('<uuid:pk>/team-advice-view/', advice.ViewTeamAdvice.as_view(), name='team_advice_view'),
    # ex: /cases/<uuid:pk>/final-advice-view/coalesce
    path('<uuid:pk>/final-advice-view/coalesce', advice.CoalesceTeamAdvice.as_view(), name='coalesce_team_advice'),
    # ex: /cases/<uuid:pk>/final-advice-view/
    path('<uuid:pk>/final-advice-view/', advice.ViewFinalAdvice.as_view(), name='final_advice_view'),
    # ex: /cases/<uuid:pk>/advice-view/give-advice/
    path('<uuid:pk>/advice-view/give-user-advice/', advice.GiveUserAdvice.as_view(), name='give_user_advice'),
    # ex: /cases/<uuid:pk>/advice-view/give-advice/approve/
    path('<uuid:pk>/advice-view/give-user-advice/<str:type>/', advice.GiveUserAdviceDetail.as_view(), name='give_user_advice_detail'),
    # ex: /cases/<uuid:pk>/advice-view/give-advice/
    path('<uuid:pk>/advice-view/give-team-advice/', advice.GiveTeamAdvice.as_view(), name='give_team_advice'),
    # ex: /cases/<uuid:pk>/advice-view/give-advice/approve/
    path('<uuid:pk>/advice-view/give-team-advice/<str:type>/', advice.GiveTeamAdviceDetail.as_view(), name='give_team_advice_detail'),
    # ex: /cases/<uuid:pk>/advice-view/give-advice/
    path('<uuid:pk>/advice-view/give-final-advice/', advice.GiveFinalAdvice.as_view(), name='give_final_advice'),
    # ex: /cases/<uuid:pk>/advice-view/give-advice/approve/
    path('<uuid:pk>/advice-view/give-final-advice/<str:type>/', advice.GiveFinalAdviceDetail.as_view(), name='give_final_advice_detail'),
    # ex: /cases/<uuid:pk>/ecju-queries/
    path('<uuid:pk>/ecju-queries/', main.ViewEcjuQueries.as_view(), name='ecju_queries'),
    # ex: /cases/<uuid:pk>/ecju-queries/add
    path('<uuid:pk>/ecju-queries/add', main.CreateEcjuQuery.as_view(), name='ecju_queries_add'),
]
