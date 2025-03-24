from django.urls import path
from .views import dashboard_view, list_users, add_user, edit_user, archive_user, archived_users, restore_user

app_name = 'dashboardadminapp'

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),  # ✅ Make sure this exists
    path('list-users/', list_users, name='list_users'),
    path('add-user/', add_user, name='add_user'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('archive-user/<int:user_id>/', archive_user, name='archive_user'),
    path('archived-users/', archived_users, name='archived_users'),
    path('restore-user/<int:user_id>/', restore_user, name='restore_user'),
]


