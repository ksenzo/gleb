from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Wallet, Game, bonus_game
from .randomizer import randomizer
import time

def game(request):
    return render(request, 'game.html', context={})


def ajax_check_user(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        wallet = Wallet.objects.get(owner=user)
        bonus_game_count = user.bonus_game_count
        user_last_game = Game.objects.filter(user=user).latest('id')
        last_game = user_last_game.amount
        response['message'] = 'account_exists'
        response['user_id'] = telegram_id
        response['last_bet'] = last_game
        response['balance'] = wallet.balance
        response['bonus_game_count'] = bonus_game_count
        print(response)
    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def ajax_check_bet_amount(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    bet_amount = request.GET.get('bet_amount')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        balance = Wallet.objects.get(owner=user).balance
        if balance == 0:
            response['message'] = 'not_enough_balance'
        elif int(bet_amount) <= balance:
            response['message'] = 'bet_amount_ok'
            print(response)
        else:
            response['message'] = 'not_enough_balance'
            print(response)
    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def ajax_start_game(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    bet_amount = request.GET.get('bet_amount')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        game = Game.objects.create(user=user, amount=int(bet_amount))
        game.start_game()
        response['message'] = 'game_starts'
        response['balance'] = Wallet.objects.get(owner=user).balance
    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def ajax_select_chest(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    choice = request.GET.get('choice')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        game = Game.objects.filter(user=user).last()
        game.choice = choice
        game.save()
        if game.winning:
            wallet = Wallet.objects.get(owner=user)
            wallet.balance += game.amount * 2
            wallet.save()

            response['winning'] = 'game_winning'

            response['balance'] = Wallet.objects.get(owner=user).balance
        else:
            response['winning'] = 'game_loosing'
            response['balance'] = Wallet.objects.get(owner=user).balance
        response['winning_amount'] = game.amount * 2
        response['message'] = 'chest_selected'
        # response['balance'] = Wallet.objects.get(owner=user).balance


    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def ajax_bonus_game(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        if user.bonus_game_count == 12:
            response['message'] = 'bonus_game_active'
        else:
            response['message'] = 'no_bonus_game'
    except User.DoesNotExist:
        response['message'] = 'no_account'
        response['message'] = 'bonus_game_active'
    return JsonResponse(response)


def ajax_start_bonus_game(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        bonus_game_list = []
        bonus_game_list = bonus_game(user)
        response['message'] = 'ok'
        response['winning'] = bonus_game_list[0]
        response['chest_2'] = bonus_game_list[1]
        response['chest_3'] = bonus_game_list[2]
    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def index(request):
    start = time.perf_counter()

    # roi = get_all_game_results()
    # games = bonus_game(201767938)
    # random_date = randomizer()
    randomizers = []
    c = 0
    t = 0
    for i in range(1, 1000):
        c += 1
        a = randomizer(30)
        randomizers.append(a)
        if a:
            t += 1
        print(f'{c}. {t / c * 100}%')
    print(time.perf_counter() - start)
    print(f'{t/c*100}%')

    return render(request,
                  'index.html',
                  context={
                      # 'roi': roi,
                      # 'games': games,
                      'randomizers': randomizers,
                  })