from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_company', views.get_company, name='get_company'),
    path('add_company', views.post_company, name='add_company'),
    path('change_company', views.patch_company, name='change_company'),
    path('del_company', views.del_company, name='del_company'),
    path('login', auth_view.LoginView.as_view(template_name='auth_form.html'), name='login'),
]
