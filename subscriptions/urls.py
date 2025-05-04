from subscriptions import views
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from .views import (
    subscription_list,
    subscription_add,
    subscription_edit,
    subscription_delete,
    user_settings,
    register,
)

urlpatterns = [
    path('', lambda request: redirect('subscription_list', permanent=False)),
    path('my/', subscription_list, name='subscription_list'),
    path('my/add/', subscription_add, name='subscription_add'),
    path('my/edit/<int:pk>/', subscription_edit, name='subscription_edit'),
    path('my/delete/<int:pk>/', subscription_delete, name='subscription_delete'),
    path('settings/', user_settings, name='user_settings'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/register/', register, name='register'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/<int:pk>/mark_paid/', views.mark_as_paid, name='mark_as_paid'),
]
