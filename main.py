import telebot
from moduls.notification_manager import send_reminders, add_reminder
import threading
import random

API_TOKEN = '6804633181:AAHcF8xA43iHIk7O5LBjvBBVYo8bxtxz1Pw'
bot = telebot.TeleBot(API_TOKEN)
reminders = {}


# Обработка команды запускаб приветствия и меню бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    welcome_message = (f"Привет, {user_first_name}! Я бот, который будет напоминать пить воду. "
                       "Используй команду /fact чтобы узнать что-то интересное о воде, "
                       "а /remind для установки напоминания.")
    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(commands=['fact'])
def fact_message(message):
    try:
        with open('moduls/wowfacts.txt', 'r', encoding='utf-8') as file:
            facts_list = file.readlines()
            random_fact = random.choice(facts_list).strip()
            bot.reply_to(message, random_fact)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


# Обработчик команды '/remind' для бота. Этот декоратор Telegram bot API указывает,
# что функция `set_reminder` будет вызвана при получении команды "/remind
@bot.message_handler(commands=['remind'])
def set_reminder(message):
    try:
        # Разделение текста сообщения на время и текст напоминания
        _, time_msg = message.text.split(maxsplit=1)  # Пропускаем команду '/remind'
        time_str, msg = time_msg.split(',', 1)  # Разбиваем строку на время и сообщение по первой запятой
        # Добавление напоминания в систему. `time_str` и `msg` получают значения времени и сообщения
        # для напоминания соответственно, оба значения очищаются от лишних пробелов с помощью метода `strip()`
        add_reminder(message.chat.id, reminders, time_str.strip(), msg.strip(), bot)
    except ValueError:
        bot.send_message(message.chat.id, "Используйте формат: /remind чч:мм, сообщение")
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, введите время и сообщение для напоминания после команды.")


# Проверка, является ли скрипт главным исполняемым файлом
if __name__ == "__main__":
    # Создание отдельного потока для функции отправки напоминаний. Создается поток для функции `send_reminders`,
    # который работает независимо от основного потока, обеспечивая тем самым асинхронную отправку напоминаний.
    reminder_thread = threading.Thread(target=send_reminders, args=(reminders, bot))
    reminder_thread.start()
    # Метод bot.polling запускает цикл, в котором бот постоянно опрашивает сервер Telegram на наличие новых сообщений,
    # что позволяет обрабатывать команды от пользователей в режиме реального времени.
    bot.polling(none_stop=True)
