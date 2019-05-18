from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('get_company/<str:company_name>/', views.get_company, name='get_company'),
    path('post_company', views.post_company, name='post_company'),
    path('change_company', views.patch_company, name='change_company'),
    path('login', auth_view.LoginView.as_view(template_name='auth_form.html'), name='login'),
    path('del_company/<str:company_name>/', views.del_company, name='del_company'),
    path('post_ad', views.post_ad, name='post_ad'),
    path('get_ad/<str:title>/', views.get_ad, name='get_ad')
]
