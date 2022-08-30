from django.shortcuts import render
from .models import *
from .randomizer import randomizer
import time


def game(request):
    return render(request, 'game.html', context={})


def index(request):
    start = time.perf_counter()

    # roi = get_all_game_results()
    # games = bonus_game(201767938)
    # random_date = randomizer()
    randomizers = []
    c = 0
    t = 0
    for i in range(1, 100000):
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
