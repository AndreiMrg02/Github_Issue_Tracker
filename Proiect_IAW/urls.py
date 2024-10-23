"""
URL configuration for Proiect_IAW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('open-issues/', views.open_issues_view, name='open_issues'),
    path('close_issues/', views.close_issues_view, name='close_issues'),
    path('create_issues/', views.create_issues_view, name='create_issues'),
    path('issues/reopen/<int:issue_id>/', views.reopen_issue, name='reopen_issue'),
    path('issues/close/<int:issue_id>/', views.close_issue, name='close_issue'),
]
