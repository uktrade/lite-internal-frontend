from django.urls import path

from users.views import users, roles

app_name = 'users'
urlpatterns = [
    # ex: /users/
    path('', users.UsersList.as_view(), name='users'),
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a user's profile
    path('<uuid:pk>/', users.ViewUser.as_view(), name='user'),
    # ex: /users/add/
    path('add', users.AddUser.as_view(), name='add'),
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/edit/
    path('<uuid:pk>/edit/', users.EditUser.as_view(), name='edit'),
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/edit/deactivate/
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/edit/reactivate/
    path('<uuid:pk>/edit/<str:status>/', users.ChangeUserStatus.as_view(), name='change_status'),
    # ex: /users/profile/ - Go to signed in user's profile
    path('profile/', users.ViewProfile.as_view(), name='profile'),

    # /users/roles/
    path('roles/', roles.Roles.as_view(), name='roles'),
]