from django.urls import path
from .views import dashboard_view, list_users, add_user

app_name = 'dashboardadminapp'  # ✅ Define app namespace

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('list-users/', list_users, name='list_users'),  # ✅ This must match your template
    path('add-user/', add_user, name='add_user'),
]
