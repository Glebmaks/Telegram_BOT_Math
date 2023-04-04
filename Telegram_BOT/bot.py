import telebot
import config
import random

from telebot import types

f = open(r'C:\Users\Gleb\Python files\Telegram_ BOT\fact.txt', 'r', encoding='UTF-8')
facts = f.read().split('\n')
f.close()

counter = 0
images = {}  # словарь для хранения списка картинок для каждого пользователя

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    global counter
    counter = 0
    images[message.chat.id] = [r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\a.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\b.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\c.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\d.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\e.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\f.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\g.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\h.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\i.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\j.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\k.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\l.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\m.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\n.png',
                                r'C:\Users\Gleb\Python files\Telegram_ BOT\pic\o.png'
                                ]
    
    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Что ты умеешь?')
    item2 = types.KeyboardButton('Расскажи интересный факт')
    item3 = types.KeyboardButton('Добавить свой факт')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Доброго времени суток👋, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданый программистом по прозвищу ✨GlebMaks✨, чтобы поведать 15 интересных фактов из жизни великих математиков.'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    global counter
    if message.chat.type == 'private':
        if message.text == 'Что ты умеешь?':
            bot.send_message(message.chat.id, 'Я могу выдать 15 интересных фактов про великих математиков! 😁')
        elif message.text == 'Расскажи интересный факт':
            if counter >= len(facts):
                counter = 0
            answer = facts[counter]
            counter += 1
            bot.send_message(message.chat.id, answer)

            # отправляем следующую картинку

            if message.chat.id in images:
                if images[message.chat.id]:
                    # добавляем первую картинку в конец списка
                    images[message.chat.id].append(images[message.chat.id][0])
                    bot.send_photo(message.chat.id, photo=open(images[message.chat.id].pop(0), 'rb'))
                else:
                    bot.send_message(message.chat.id, 'Картинок больше нет')
            else:
                bot.send_message(message.chat.id, 'Ошибка: список картинок не найден')

        elif message.text == 'Добавить свой факт':
            bot.send_message(message.chat.id, 'Напишите свой факт')
            bot.register_next_step_handler(message, process_fact)
        else:
             bot.send_message(message.chat.id, 'Я не знаю что ответить 😣')
def process_fact(message):
    with open('new_facts.txt', 'a', encoding='UTF-8') as f:
        f.write(message.text + '\n')
    bot.send_message(config.ADMIN_CHAT_ID, 'Пользователь {} {} отправил новый факт: "{}"'.format(message.from_user.first_name, message.from_user.last_name, message.text))
    bot.send_message(message.chat.id, 'Спасибо за ваш факт. Мы добавим его после проверки администрацией.')

bot.polling(non_stop=True, interval=0)