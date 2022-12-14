from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Wallet, Game, bonus_game, reset_keys, Casino
from .randomizer import randomizer
import time

def game(request):
    return render(request, 'game.html', context={})


def ajax_check_user(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        if user.keys < 0:
            user.keys = 0
            user.save()
        keys = user.keys
        wallet = Wallet.objects.get(owner=user)
        if user.bonus_game_count == 0 and user.keys > 0:
            bonus_game_count = 0
        else:
            bonus_game_count = user.bonus_game_count
        if Game.objects.filter(user=user).exists():
            user_last_game = Game.objects.filter(user=user).latest('id')
            last_game = user_last_game.amount
            response['last_bet'] = last_game
        response['message'] = 'account_exists'
        response['user_id'] = telegram_id
        response['balance'] = wallet.balance
        response['bonus_game_count'] = bonus_game_count
        response['keys'] = user.keys

    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)

def key_null_throw(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        keys = reset_keys(user)
        response['message'] = keys
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
    return JsonResponse(response, safe=False)


def ajax_select_chest(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    choice = request.GET.get('choice')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        game = Game.objects.filter(user=user).last()
        game.choice = choice
        game.save()
        casino = Casino.objects.get_or_create()

        if game.key_win:
            if user.keys < 6:
                user.keys += 1
                user.save()
            else:
                pass
            response['keys'] = user.keys
            response['key_result'] = 'key_winning'
        else:
            response['key_result'] = 'key_lose'

        if game.winning:
            casino[0].casinoLose(telegram_id)
            wallet = Wallet.objects.get(owner=user)
            wallet.balance += game.amount * 2
            wallet.save()
            response['currentBalance'] = casino[0].currentBalance
            response['returnBalance'] = casino[0].returnBalance
            response['winning'] = 'game_winning'
            response['balance'] = Wallet.objects.get(owner=user).balance
        else:
            casino[0].casinoWin(telegram_id)
            response['winning'] = 'game_loosing'
            response['returnBalance'] = casino[0].returnBalance
            response['currentBalance'] = casino[0].currentBalance
            response['balance'] = Wallet.objects.get(owner=user).balance

        response['winning_amount'] = game.amount * 2
        response['message'] = 'chest_selected'
        response['balance'] = Wallet.objects.get(owner=user).balance


    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def ajax_bonus_game(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        if user.bonus_game_count == 0 and user.keys > 0:
            response['bonus_game_count'] = user.bonus_game_count
            response['message'] = 'bonus_game_active'
            response['keys'] = user.keys
        else:
            response['bonus_game_count'] = user.bonus_game_count
            response['keys'] = user.keys
            response['message'] = 'no_bonus_game'
    except User.DoesNotExist:
        response['message'] = 'no_account'
    return JsonResponse(response)


def ajax_start_bonus_game(request):
    response = dict()
    telegram_id = request.GET.get('telegram_id')
    try:
        user = User.objects.get(telegram_id=telegram_id)
        casino, created = Casino.objects.get_or_create()
        bonus_game_list = []
        bonus_game_list = bonus_game(user)
        casino.saveCasino(bonus_game_list[4], bonus_game_list[3])
        if user.keys < 0:
            user.keys = 0
        user.save()
        user.keys = int(user.keys) - 1
        user.save()
        response['bonus_game_count'] = user.bonus_game_count
        response['message'] = 'win'
        response['winning'] = bonus_game_list[0]
        response['avarage'] = bonus_game_list[1]
        response['perc'] = bonus_game_list[2]
        response['current'] = bonus_game_list[3]
        response['return'] = bonus_game_list[4]
        response['win_sum'] = bonus_game_list[5]
        response['keys'] = user.keys
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