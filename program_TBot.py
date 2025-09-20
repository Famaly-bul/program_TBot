import telebot
import random
import os
import json
import re

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен Telegram-бота не найден! Установите переменную окружения TELEGRAM_BOT_TOKEN.")
bot = telebot.TeleBot(TOKEN)

HELP = (
    "/help - Напечатать справку по программе.\n"
    "/add <дата> <задача> - Добавить задачу на дату.\n"
    "/show <дата> - Показать задачи на дату.\n"
    "/showall - Показать все задачи.\n"
    "/random <дата> - Добавить случайное место на дату.\n"
)

RANDOM_TASKS = [
    "Парк Горького", "ВДНХ", "Красная площадь", "Патриаршие пруды", "Царицыно",
    "Сокольники", "Музеон", "Парк Зарядье", "Воробьёвы горы", "Новодевичий пруд",
    "Парк Победы", "Аптекарский огород", "Ботанический сад МГУ", "Останкинский парк",
    "Парк Фили", "Парк Кузьминки", "Парк Северное Тушино", "Парк Измайлово",
    "Парк Лосиный остров", "Парк Коломенское", "Парк Садовники", "Парк Бабушкинский",
    "Парк Перловский", "Парк Дружбы", "Парк Олимпийской деревни", "Парк Тропарёво",
    "Парк Школьный", "Парк Лианозовский", "Парк Ангарские пруды", "Парк Яуза",
    "Парк Митино", "Парк Сосенки", "Парк Малевича (Подмосковье)", "Парк Мещерский (Подмосковье)",
    "Парк Валуевский (Подмосковье)", "Парк Середниково (Подмосковье)", "Парк Архангельское (Подмосковье)",
    "Парк Абрамцево (Подмосковье)", "Парк Звенигород (Подмосковье)", "Парк Лесная сказка (Подмосковье)",
    "Парк Пехорка (Подмосковье)", "Парк Радуга (Подмосковье)", "Парк Дубрава (Подмосковье)",
    "Парк Воскресенское (Подмосковье)", "Парк Лосиный остров (Подмосковье)", "Парк Солнечная поляна (Подмосковье)",
    "Парк Сказка (Подмосковье)", "Парк Кусково", "Парк Раменки", "Парк Тушино"
]

TASKS_FILE = "tasks.json"

def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)

def load_tasks():
    global tasks
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = {}

load_tasks()

tasks = {}

def is_valid_date(date):
    return re.match(r"\d{2}\.\d{2}(\.\d{4})?$", date) is not None

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add_task(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(message.chat.id, "Используйте: /add <дата> <задача>")
        return
    date = parts[1].strip()
    task = parts[2].strip()
    if not is_valid_date(date):
        bot.send_message(message.chat.id, "Дата должна быть в формате ДД.ММ или ДД.ММ.ГГГГ")
        return
    tasks.setdefault(date, []).append(task)
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена на дату {date}.")
    save_tasks()

@bot.message_handler(commands=["show"])
def show_tasks(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Используйте: /show <дата>")
        return
    date = parts[1].strip()
    if not is_valid_date(date):
        bot.send_message(message.chat.id, "Дата должна быть в формате ДД.ММ или ДД.ММ.ГГГГ")
        return
    if date in tasks and tasks[date]:
        text = f"{date.upper()}:\n"
        for task in tasks[date]:
            text += f"- {task}\n"
    else:
        text = "Задач на эту дату нет."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["showall"])
def show_all_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id, "Список задач пуст.")
        return
    text = ""
    for date, task_list in tasks.items():
        text += f"{date}:\n"
        for task in task_list:
            text += f"  - {task}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["random"])
def add_random_task(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Используйте: /random <дата>")
        return
    date = parts[1].strip()
    if not is_valid_date(date):
        bot.send_message(message.chat.id, "Дата должна быть в формате ДД.ММ или ДД.ММ.ГГГГ")
        return
    task = random.choice(RANDOM_TASKS)
    tasks.setdefault(date, []).append(task)
    bot.send_message(message.chat.id, f"Случайное место '{task}' добавлено на дату {date}.")
    save_tasks()

@bot.message_handler(commands=["delete"])
def delete_task(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(message.chat.id, "Используйте: /delete <дата> <номер_задачи>")
        return
    date = parts[1].strip()
    try:
        idx = int(parts[2].strip()) - 1
        if date in tasks and 0 <= idx < len(tasks[date]):
            removed = tasks[date].pop(idx)
            save_tasks()
            bot.send_message(message.chat.id, f"Задача '{removed}' удалена с даты {date}.")
        else:
            bot.send_message(message.chat.id, "Неверная дата или номер задачи.")
    except ValueError:
        bot.send_message(message.chat.id, "Номер задачи должен быть числом.")

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот-планировщик. Введите /help для списка команд.")

bot.polling(none_stop=True)