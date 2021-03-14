"""Adventure_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from character import views as character_views
from combat import views as combat_views
from ui import views as ui_views
from storyboard import views as storyboard_views
#from game_data import game_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ui_views.home , name='main-page'),
    path('login/', ui_views.login , name='login'),
    path('logout/', ui_views.logout , name='logout'),
    path('register/', ui_views.register , name='register'),
    path('pc_character/<int:character_id>/', character_views.show_pc_character, name='view-pc-char'),
    path('npc_character/<int:character_id>/', character_views.show_npc_character, name='view-npc-char'),
    path('combat/init/', combat_views.init_combat, name='init-combat'),
    path('combat/turn/', combat_views.init_turn, name='init_turn'),
    path('combat/positions/', combat_views.get_positions, name='combat-positions'),
    path('combat/attack', combat_views.do_attack, name='combat-attack'),
    path('script/', storyboard_views.get_script, name='get-script'), 
    path('script/<script_id>', storyboard_views.get_script, name='get-script_id'),
    path('script/<script_id>/<response_id>', storyboard_views.handle_response, name='handle_response')
]   
