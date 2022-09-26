from django.urls import path, re_path
from .views import game, index, ajax_check_user, ajax_check_bet_amount, ajax_start_game, ajax_select_chest, ajax_bonus_game, ajax_start_bonus_game

urlpatterns = [
    path('', game),
    path('test', index),
    path('ajax_check_user', ajax_check_user),
    path('ajax_check_bet_amount', ajax_check_bet_amount),
    path('ajax_start_game', ajax_start_game),
    path('ajax_select_chest', ajax_select_chest),
    path('ajax_bonus_game', ajax_bonus_game),
    path('ajax_start_bonus_game', ajax_start_bonus_game),


]
