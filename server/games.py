from server.models import Game, BonusGame
from randomizer import randomizer


# def bonus_game(user):
#     user_games = Game.objects.filter(user=user).order_by('-id')[:20]
#     game_amount = 0
#     for game in user_games:
#         game_amount += game.amount
#     average_amount = game_amount/20
#     game = BonusGame.objects.create(user=user, amount=average_amount)
#     if randomizer(4):
#         game.winning_amount = round(average_amount * 10)
#     elif randomizer(24):
#         game.winning_amount = round(average_amount)
#     else:
#         game.winning_amount = round(average_amount * 0.5)
#     game.save()
#     # chest_1 = round(average_amount * 0.5)
#     # chest_2 = round(average_amount)
#     # chest_3 = round(average_amount * 10)
#
#     return game.winning_amount

# from bot.settings import BASE_DIR, MEDIA_ROOT
# from bot.settings import STATIC_ROOT


# def draw_boxes(game, amount):
#     user = game.user
#     if game.demo_game:
#         wallet = DemoWallet.objects.get(owner=user)
#     else:
#         wallet = Wallet.objects.get(owner=user)
#
#     im = Image.open(os.path.join(STATIC_ROOT, 'chest_2.gif'))
#     frames = []
#     font_type = ImageFont.truetype(f'{BASE_DIR}/fonts/arial.ttf', 28)
#     for frame in ImageSequence.Iterator(im):
#         frame = frame.convert('RGB')
#
#         d = ImageDraw.Draw(frame)
#         if game.winning:
#             if game.choice == 'left':
#                 d.text(xy=(160, 120), text=f'{2*amount}', fill=(255, 69, 0), font=font_type)
#             elif game.choice == 'right':
#                 d.text(xy=(420, 120), text=f'{2*amount}', fill=(255, 69, 0), font=font_type)
#         else:
#             if game.choice == 'left':
#                 d.text(xy=(420, 120), text=f'{2*amount}', fill=(255, 69, 0), font=font_type)
#             elif game.choice == 'right':
#                 d.text(xy=(160, 120), text=f'{2*amount}', fill=(255, 69, 0), font=font_type)
#         del d
#         b = io.BytesIO()
#         frame.save(b, format='GIF')
#         frame = Image.open(b)
#         frames.append(frame)
#     path = os.path.join(MEDIA_ROOT, f'{game.pk} - {game.amount}.gif')
#     # print(path)
#     frames[0].save(path, save_all=True, append_images=frames[1:])
#     if game.winning:
#         wallet.balance += int(amount)
#         wallet.save()
#     else:
#         wallet.balance -= int(amount)
#         wallet.save()
#     # with open(path, 'r') as f:
#     #     gif = f
#     # # gif = open(path, 'rb')
#     # print(gif)
#     return path


# def randomizer(winning_percent):
#     fake = Faker()
#     start_date = datetime.date(year=1001, month=1, day=1)
#     end_date = datetime.date(year=2999, month=12, day=31)
#     random_date_1 = fake.date_between(start_date=start_date, end_date=end_date)
#     random_date_2 = fake.date_between(start_date=start_date, end_date=end_date)
#     int_random_date_1 = random_date_1.day * random_date_1.month * random_date_1.year
#     int_random_date_2 = random_date_2.day * random_date_2.month * random_date_2.year
#     random_time = fake.unix_time()
#
#     random_int = int_random_date_1 * int_random_date_2 + random_time
#     winning_range_start = random.randint(1, random_int)
#     count_winning_combinations = int((random_int * (winning_percent / 100)).__round__(0))
#
#     players_number = random.randint(1, random_int)
#
#     x = winning_range_start + int(count_winning_combinations)
#     if x < random_int:
#         winning_combinations = range(winning_range_start, x)
#         if players_number in winning_combinations:
#             return True
#         else:
#             return False
#     else:
#         winning_combinations_1 = range(winning_range_start, random_int + 1)
#         len_of_second_part = int(count_winning_combinations) - len(winning_combinations_1)
#         winning_combinations_2 = range(1, len_of_second_part + 1)
#         if players_number in winning_combinations_1:
#             return True
#         elif players_number in winning_combinations_2:
#             return True
#         else:
#             return False


# def start_gaming_process(user, amount):
#     game = Game.objects.create(user=user, amount=amount)
#     wallet = Wallet.objects.get(owner=user)
#     win_or_lose = random.randint(0, 9)
#
#     if win_or_lose in (7, 8, 9):
#         game.winning = True
#         game.save()
#         # box = draw_box(game, amount)
#     else:
#         game.winning = False
#         game.save()
#         # box = draw_box(game, amount)
#
#
# def start_demo_gaming_process(user, amount):
#     game = Game.objects.create(user=user, amount=amount, demo_game=True)
#     wallet = DemoWallet.objects.get(owner=user)
#     win_or_lose = random.randint(0, 9)
#
#     if win_or_lose in (4, 5, 6, 7, 8, 9):
#         game.winning = True
#         game.save()
#         # box = draw_box(game, amount)
#     else:
#         game.winning = False
#         game.save()
#         # box = draw_box(game, amount)

# def select_box():
#     path = os.path.join(STATIC_ROOT, 'chest_1.gif')
#     return path


