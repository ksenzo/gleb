from time import sleep
import re

from django.core.management.base import BaseCommand
from django.conf import settings

import telebot
from telebot import types

import random

from server.models import User, Wallet, PaymentMethod, Payment, Game, DemoWallet
from server.games import start_gaming_process, select_box, draw_boxes, start_demo_gaming_process


class Command(BaseCommand):
    help = 'TG-bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TG_TOKEN)

        @bot.message_handler(commands=['start'])
        def start(message):
            User.objects.get_or_create(telegram_id=message.from_user.id,
                                       username=message.from_user.id,
                                       first_name=message.from_user.first_name)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            demo_game = types.KeyboardButton('🎮Демо игра')

            markup.add(start_game, balance, demo_game, row_width=2)

            mess = f'<b>{message.from_user.first_name}</b>, начни игру прямо сейчас!'
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        def show_balance(message):
            user = User.objects.get(telegram_id=message.from_user.id)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            make_deposit = types.KeyboardButton('💳Депозит')
            demo_game = types.KeyboardButton('🎮Демо игра')

            markup.add(make_deposit, start_game, demo_game, row_width=2)

            mess = f'<b>{message.from_user.first_name}</b>, на вашем балансе {Wallet.objects.get(owner=user).balance} тестовых рублей'
            # print(mess)
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        def start_demo_game(message):
            user = User.objects.get(telegram_id=message.from_user.id)
            try:
                wallet = DemoWallet.objects.get(owner=user)
            except DemoWallet.DoesNotExist:
                wallet = DemoWallet.objects.create(owner=user)

            markup = types.InlineKeyboardMarkup(row_width=3)
            bet_100 = types.InlineKeyboardButton('100', callback_data='demo_bet_100')
            bet_500 = types.InlineKeyboardButton('500', callback_data='demo_bet_500')
            bet_1000 = types.InlineKeyboardButton('1000', callback_data='demo_bet_1000')
            bet_choice = types.InlineKeyboardButton('Другой размер ставки', callback_data='bet_choice')
            markup.add(bet_100, bet_500, bet_1000, bet_choice)
            mess = bot.send_message(message.chat.id,
                                    f'<b>{message.from_user.first_name}</b>, на вашем балансе: <b>{wallet.balance}</b> тестовых рублей\nВыберите размер ставки:',
                                    parse_mode='html',
                                    reply_markup=markup)
            bot.register_next_step_handler(mess, demo_bet_size_selection)

        @bot.callback_query_handler(func=lambda callback: callback.data)
        def demo_bet_size_selection(callback):
            user = User.objects.get(telegram_id=callback.message.chat.id)
            wallet_balance = DemoWallet.objects.get(owner=user).balance
            if callback.data == 'bet_choice':
                mess = bot.send_message(callback.message.chat.id, 'Напишите размер ставки:')
            elif callback.data in ('demo_bet_100', 'demo_bet_500', 'demo_bet_1000'):
                amount_list = (re.findall(r'\d+', callback.data))
                amount = int(amount_list[0])
                if amount <= wallet_balance:
                    start_demo_gaming_process(user, amount)
                    img = select_box()
                    with open(img, 'rb') as f:
                        bot.send_animation(callback.message.chat.id, f)
                        f.close()

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    left = types.InlineKeyboardButton('👈левый', callback_data='left')
                    right = types.InlineKeyboardButton('👉правый', callback_data='right')
                    markup.add(left, right)
                    bot.send_message(callback.message.chat.id, 'Выберите сундук', parse_mode='html', reply_markup=markup)
            elif callback.data in ('left' or 'right'):
                print('hello')
                choice = callback.data
                game = Game.objects.filter(user=user).last()
                game.choice = choice
                game.save()
                img = draw_boxes(game, game.amount)
                with open(img, 'rb') as f:
                    bot.send_animation(callback.message.chat.id, f)
                    f.close()
                if game.winning:
                    mess = f'Поздравляем, вы выиграли {2*game.amount}!'
                else:
                    mess = 'Вам не повезло, в следующий раз повезёт!'
                bot.send_message(callback.message.chat.id, mess)

        def deposit(message):
            user = User.objects.get(telegram_id=message.from_user.id)
            wallet = Wallet.objects.get(owner=user)
            wallet.balance += 1000
            wallet.save()
            mess = f'На данный момент игра на реальные деньги недоступна'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            demo_game = types.KeyboardButton('🎮Демо игра')

            markup.add(start_game, balance, demo_game, row_width=2)

            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        def bet_size_selection(message):
            user = User.objects.get(telegram_id=message.from_user.id)
            try:
                Wallet.objects.get(owner=user)
            except Wallet.DoesNotExist:
                Wallet.objects.create(owner=user, currency='RUB')
            mess = bot.send_message(message.chat.id, 'Напишите размер ставки', parse_mode='html')
            bot.register_next_step_handler(mess, chose_box)

        def chose_box(message):
            amount = message.text
            wallet_balance = Wallet.objects.get(owner=User.objects.get(telegram_id=message.from_user.id)).balance
            if int(amount) <= wallet_balance:
                user = User.objects.get(telegram_id=message.from_user.id)
                start_gaming_process(user, amount)
                img = select_box()
                with open(img, 'rb') as f:
                    bot.send_animation(message.chat.id, f)
                    f.close()

                markup = types.InlineKeyboardMarkup(row_width=2)
                left = types.InlineKeyboardButton('👈левый', callback_data='left')
                right = types.InlineKeyboardButton('👉правый', callback_data='right')
                markup.add(left, right)
                bot.send_message(message.chat.id, 'Выберите сундук', parse_mode='html', reply_markup=markup)
                # bot.register_next_step_handler(mess, game_result)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                make_deposit = types.KeyboardButton('💳Депозит')
                start_game = types.KeyboardButton('🎲Начать игру')
                markup.add(make_deposit, start_game, row_width=2)
                bot.send_message(message.chat.id,
                                 f'Ваш баланс <b>{wallet_balance} rub</b>\nПополните счёт!',
                                 parse_mode='html',
                                 reply_markup=markup)


        def game_result(message):
            amount = message.text
            user = User.objects.get(telegram_id=message.from_user.id)
            img = start_gaming_process(user, amount)
            with open(img, 'rb') as f:
                bot.send_animation(message.chat.id, f)
                f.close()

        # @bot.callback_query_handler(func=lambda callback: callback.data)
        # def check_callback_currency(callback):
        #     user = User.objects.get(telegram_id=callback.message.chat.id)
            # if callback.data in ('left' or 'right'):
            #     choice = callback.data
            #     game = Game.objects.filter(user=user).last()
            #     game.choice = choice
            #     game.save()
            #     img = draw_boxes(game, game.amount)
            #     with open(img, 'rb') as f:
            #         bot.send_animation(callback.message.chat.id, f)
            #         f.close()
            #     if game.winning:
            #         mess = f'Поздравляем, вы выиграли {2*game.amount}!'
            #     else:
            #         mess = 'Вам не повезло, в следующий раз повезёт!'
            #     bot.send_message(callback.message.chat.id, mess)

        @bot.message_handler(commands=["test"])
        def test(message):
            bot.send_message(message.chat.id, 'test')
            print(message.chat)


        @bot.message_handler(content_types=["text"])
        def message(message):
            if message.text == '🎲Начать игру':
                bet_size_selection(message)
            elif message.text == '💰Баланс':
                show_balance(message)
            elif message.text == '💳Депозит':
                deposit(message)
            elif message.text == '🎮Демо игра':
                start_demo_game(message)

        bot.infinity_polling(timeout=10, long_polling_timeout=5)
