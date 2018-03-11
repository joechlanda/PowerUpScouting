"""PowerUpScouter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path

from scorer import views

urlpatterns = [
	re_path('^$', views.home, name='home'),
	#re_path('^update_frc/(?P<event>[\w.@+-]+)/', views.update_frc, name='update_frc'),
	path('update_frc/', views.update_frc, name='update_frc'),
	path('teams/', views.teams, name='teams'),
	re_path(r'^teams/(?P<number>\d+)/$', views.team_summary, name='team_summary'),
    path('admin/', admin.site.urls),
    path('teams/efficiency/', views.efficiency_update, name='team_efficiency'),
    path('match', views.matches, name='matches'),
    re_path('match/(?P<number>\d+)/$', views.match, name='match'),
    re_path('match/(?P<number>\d+)/edit', views.match_edit, name='match_edit')
]
