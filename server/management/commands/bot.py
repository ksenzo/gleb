from time import sleep
import re

from django.core.management.base import BaseCommand
from django.conf import settings

import telebot
from telebot import types

import random

from server.models import User, Wallet, PaymentMethod, Payment, Game, DemoWallet


class Command(BaseCommand):
    help = 'TG-bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TG_TOKEN)

        @bot.message_handler(commands=['start'])
        def start(message):
            user, _ = User.objects.get_or_create(telegram_id=message.from_user.id,
                                                 username=message.from_user.id,
                                                 first_name=message.from_user.first_name)
            wallet = Wallet.objects.get(owner=user)
            wallet.balance = 0
            wallet.save()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            make_deposit = types.KeyboardButton('💳Депозит')
            rules = types.KeyboardButton('📙Правила')
            markup.add(start_game, rules, balance, make_deposit, row_width=2)

            mess = f'<b>{message.from_user.first_name}</b>, начни игру прямо сейчас!'
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        def show_balance(message):
            user = User.objects.get(telegram_id=message.from_user.id)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            make_deposit = types.KeyboardButton('💳Депозит')
            rules = types.KeyboardButton('📙Правила')
            markup.add(start_game, rules, balance, make_deposit, row_width=2)

            mess = f'<b>{message.from_user.first_name}</b>, на вашем балансе {Wallet.objects.get(owner=user).balance} рублей'
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        def deposit(message):
            user = User.objects.get(telegram_id=message.from_user.id)
            wallet = Wallet.objects.get(owner=user)
            wallet.balance += 10000
            wallet.save()
            mess = f'На ваш счёт добавлено 10000 рублей'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            make_deposit = types.KeyboardButton('💳Депозит')
            rules = types.KeyboardButton('📙Правила')
            markup.add(start_game, rules, balance, make_deposit, row_width=2)

            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        def start_game(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            make_deposit = types.KeyboardButton('💳Депозит')
            rules = types.KeyboardButton('📙Правила')
            markup.add(start_game, rules, balance, make_deposit, row_width=2)
            bot.send_message(message.chat.id, '👇Нажми, что бы начать играть', parse_mode='html', reply_markup=markup)

        def rules(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_game = types.KeyboardButton('🎲Начать игру')
            balance = types.KeyboardButton('💰Баланс')
            make_deposit = types.KeyboardButton('💳Депозит')
            rules = types.KeyboardButton('📙Правила')
            markup.add(start_game, rules, balance, make_deposit, row_width=2)
            mess = '''Предупреждение ⚠️
«FirstBoxBot» - азартная игра! Этот бот несет развлекательный характер, не злоупотребляйте азартными играми .

С уважением ,администрация

Правила:

«FirstBoxBot» предлагает сыграть в очень простую и интересную игру!😲
Испытай свою удачу ,угадав один из пиратских сундуков🏴‍☠️- твоя ставка удвоиться💷! Но стоит тебе сделать неверный выбор и тебе достанется пустой сундук 💸.

Как это работает ?

Предположим ставка составляет 1000₽
Выбрав правильный сундук - получим 2000₽ (то есть х2 от нашей ставки) , в противоположном случае наша ставка сгорает .

⚠️ Что бы лучше усвоить правила
«FirstBoxBot» предлагает сыграть в «демо игру»
            '''
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

        @bot.message_handler(commands=["test"])
        def test(message):
            bot.send_message(message.chat.id, 'test')
            print(message.chat)

        @bot.message_handler(content_types=["text"])
        def message(message):
            if message.text == '🎲Начать игру':
                start_game(message)
            elif message.text == '💰Баланс':
                show_balance(message)
            elif message.text == '💳Депозит':
                deposit(message)
            elif message.text == '📙Правила':
                rules(message)

        bot.infinity_polling(timeout=10, long_polling_timeout=5)
