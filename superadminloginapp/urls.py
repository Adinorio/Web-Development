from django.urls import path
from .views import login_view,logout_view

app_name= 'superadminloginapp'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout_view'),
]
