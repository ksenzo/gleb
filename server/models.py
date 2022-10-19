from django.db import models
from django.contrib.auth.models import AbstractUser
from .randomizer import randomizer


class User(AbstractUser):
    telegram_id = models.IntegerField(primary_key=True)
    # username = telegram_id
    new_user = models.BooleanField(default=True)
    new_game_count = models.IntegerField(default=0)
    bonus_game_count = models.IntegerField(default=0)
    keys = models.IntegerField(default=0)

    def __str__(self):
        return str(self.telegram_id)

class Casino(models.Model):
    hightVal = models.IntegerField(default=100000)
    currentBalance = models.IntegerField(default=100000)
    returnBalance = models.IntegerField(default=0)

    def casinoWin(self, telegram_id):
        user = User.objects.get(telegram_id=telegram_id)
        game = Game.objects.filter(user=user).last()
        if self.currentBalance >= self.hightVal * 2:
            self.currentBalance = 100000
            self.returnBalance = 0
            self.save()
        self.currentBalance += game.amount
        self.save()

    def casinoLose(self, telegram_id):
        user = User.objects.get(telegram_id=telegram_id)
        game = Game.objects.filter(user=user).last()
        self.currentBalance -= game.amount * 2
        self.returnBalance += game.amount * 2
        self.save()

class Wallet(models.Model):
    CURRENCY_CHOICES = [
        ('USD', '$ USD'),
        ('EUR', '€ EUR'),
        ('USDT', 'USD₮'),
        ('UAH', '₴ UAH'),
        ('RUB', '₽ RUB'),
        ('KZT', '₸ KZT'),
        ('AMD', '֏ AMD'),
        ('AZN', '₼ AZN'),
        ('BYN', 'Br BYN')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(default=0)
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, default='RUB')


class DemoWallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(default=10000)


class PaymentMethod(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Payment(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class BonusGame(models.Model):
    GAME_CHOICES = (
        ('left', 'left'),
        ('middle', 'middle'),
        ('right', 'right')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    winning = models.BooleanField(default=False)
    winning_amount = models.IntegerField(null=True)
    choice = models.CharField(max_length=6, choices=GAME_CHOICES)
    demo_game = models.BooleanField(default=False)


class Game(models.Model):
    GAME_CHOICES = (
        ('left', 'left'),
        ('right', 'right')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    winning = models.BooleanField(default=False)
    choice = models.CharField(max_length=5, choices=GAME_CHOICES)
    demo_game = models.BooleanField(default=False)
    key_win = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} | {self.winning}'

    # def new_user_winning(self):
    #     if self.user.new_user:
    #         if self.amount <= 100:
    #             if self.user.game_set <= 3:
    #                 self.winning = True
    #         elif 100 < self.amount < 200:
    #             if self.user.game_set <= 2:
    #                 self.winning = True
    #         elif self.amount >= 200:
    #             if self.user.game_set <= 1:
    #                 self.winning = True

    def start_game(self):
        wallet = Wallet.objects.get(owner=self.user)
        wallet.balance -= self.amount
        wallet.save()
        casino = Casino.objects.get_or_create()
        current_balance = casino[0].currentBalance
        return_balance = casino[0].returnBalance
        hight_val = casino[0].hightVal

        if self.user.new_game_count == 3:
            self.user.new_user = False
        if self.user.new_user:
            self.user.new_game_count += 1
            if self.amount <= 100:
                if self.user.new_game_count <= 3:
                    self.winning = True
                    self.key_win = True
            elif 100 < self.amount < 200:
                if self.user.new_game_count <= 2:
                    self.winning = True
                    self.key_win = True
            elif self.amount >= 200:
                if self.user.new_game_count <= 1:
                    self.winning = True
                    self.key_win = True
        else:
            if self.user.keys == 0:
                self.key_win = randomizer(40 * change_roi_of_game())
            elif self.user.keys == 1:
                self.key_win = randomizer(50 * change_roi_of_game())
            elif self.user.keys == 2:
                self.key_win = randomizer(30 * change_roi_of_game())
            elif self.user.keys == 3:
                self.key_win = randomizer(30 * change_roi_of_game())
            elif self.user.keys == 4:
                self.key_win = randomizer(30 * change_roi_of_game())
            elif self.user.keys == 5:
                self.key_win = randomizer(30 * change_roi_of_game())
            else:
                pass

            if return_balance < hight_val * 0.8:
                if self.amount <= 100:
                    self.winning = randomizer(60 * change_roi_of_game())
                elif 500 > self.amount > 100:
                    self.winning = randomizer(50 * change_roi_of_game())
                else:
                    self.winning = randomizer(50 * change_roi_of_game())
            elif return_balance >= hight_val * 0.8:
                self.winning = randomizer(0 * change_roi_of_game())

        self.user.bonus_game_count += 1
        if self.user.bonus_game_count == 12:
            bonus_game(self.user)
            self.user.bonus_game_count = 0
        self.user.save()
        self.save()

def reset_keys(user):
    user = user
    user.keys = 0
    user.save()

    return user.keys

dynamic_percents = [1, 19, 30, 29, 50, 20]
dynamic_factors = [100, 10, 1, 1.5, 0.5, 0.1]

def bonus_game(user):
    global dynamic_percents
    global dynamic_factors
    user_games = Game.objects.filter(user=user).order_by('-id')[:12]
    game_amount = 0
    casino = Casino.objects.get_or_create()
    current_balance = casino[0].currentBalance
    return_balance = casino[0].returnBalance
    hight_val = casino[0].hightVal

    for game in user_games:
        game_amount += game.amount
    average_amount = game_amount/12
    keys = user.keys
    game = BonusGame.objects.create(user=user, amount=average_amount)

    if return_balance < hight_val * 0.8:
        for idx, x in enumerate(dynamic_percents):
            if randomizer(x):
                game.winning_amount = round(average_amount * dynamic_factors[idx])
                return_balance += round(average_amount * dynamic_factors[idx])
                current_balance -= round(average_amount * dynamic_factors[idx])
                del dynamic_percents[idx]
                del dynamic_factors[idx]
                casino[0].save()
                break
            else:
                game.winning_amount = round(average_amount * 0)
        game.save()
    elif return_balance >= hight_val * 0.8:
        if randomizer(100):
            game.winning_amount -= round(average_amount * 0)
        else:
            game.winning_amount -= round(average_amount * 0)

        if current_balance >= hight_val * 2:
           return_balance = 0
           current_balance = 100000
           casino[0].save()

        game.save()

    if keys == 1:
       dynamic_percents = [1, 19, 30, 29, 50, 20]
       dynamic_factors = [100, 10, 1, 1.5, 0.5, 0.1]

    user = user
    user.bonus_game_count = 0
    user.save()

    wallet = Wallet.objects.get(owner=user)
    wallet.balance += game.winning_amount
    wallet.save()

    return game.winning_amount, average_amount, dynamic_factors, current_balance, return_balance


def get_all_game_results():
    games = Game.objects.all()
    total_amount, total_winnings, total_games, total_winning_games = [0] * 4
    for game in games:
        total_games += 1
        total_amount += game.amount
        if game.winning:
            total_winning_games += 1
            total_winnings += (game.amount * 2)
    profit = total_amount - total_winnings
    casino_roi = (profit / total_amount) * 100
    return casino_roi


def change_roi_of_game():
    # casino_roi = get_all_game_results()
    casino_roi = 40
    if casino_roi >= 40:
        winning_chance = 1
    elif 36 <= casino_roi < 40:
        winning_chance = 0.8
    elif 30 <= casino_roi < 36:
        winning_chance = 0.5
    else:
        winning_chance = 0.2
    return winning_chance