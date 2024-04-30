import datetime
import time
import logging


# Функция для отправки напоминаний в соответствии с текущим временем
def send_reminders(reminders, bot):
    while True:  # Бесконечный цикл, чтобы функция продолжала проверять время и отправлять напоминания
        try:
            now = datetime.datetime.now().strftime('%H:%M')  # Получение текущего времени в формате часы:минуты
            to_delete = []  # Список для времени напоминаний, которые нужно будет удалить после отправки
            for reminder_time, chat_info in list(reminders.items()):
                if reminder_time == now:  # Проверка, соответствует ли время напоминания текущему времени
                    for chat_id, message in chat_info:
                        bot.send_message(chat_id, message)  # Отправка сообщения
                    to_delete.append(reminder_time)  # Добавление времени напоминания в список на удаление

            for key in to_delete:
                del reminders[key]  # Удаление напоминаний, которые уже были отправлены

            time.sleep(5)  # Ожидание перед следующей проверкой, чтобы не загружать систему
        except Exception as e:
            logging.error(f"Error in send_reminders: {e}")  # Логирование ошибок


# Функция проверки корректности формата времени
def check_time_format(time_str):
    try:
        datetime.datetime.strptime(time_str, '%H:%M')  # Попытка преобразовать строку в дату
        return True
    except ValueError:
        return False  # Возврат False, если формат времени неверен


# Функция нормализации времени для избежания ошибок ввода пользователем
def normalize_time(time_str):
    hour, minute = map(int, time_str.split(':'))  # Разделение строки на часы и минуты
    hour = max(0, min(23, hour))  # Корректировка часов в допустимый диапазон
    minute = max(0, min(59, minute))  # Корректировка минут в допустимый диапазон
    return f"{hour:02d}:{minute:02d}"  # Форматирование и возврат корректного времени


# Функция добавления напоминания в систему
def add_reminder(chat_id, reminders, time_str, message, bot):
    if not check_time_format(time_str):
        bot.send_message(chat_id, "Неверный формат времени. Введите время в формате 'чч:мм'")
        return

    time_str = normalize_time(time_str)  # Нормализация введенного времени
    if time_str in reminders:
        reminders[time_str].append((chat_id, message))  # Добавление напоминания, если время уже есть в словаре
    else:
        reminders[time_str] = [(chat_id, message)]  # Создание нового списка напоминаний для нового времени
    bot.send_message(chat_id, f"Напоминание '{message}' на {time_str} установлено.")  # Информирование пользователя
