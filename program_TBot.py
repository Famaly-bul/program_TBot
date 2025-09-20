import telebot
import random
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
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

tasks = {}

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
    tasks.setdefault(date, []).append(task)
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена на дату {date}.")

@bot.message_handler(commands=["show"])
def show_tasks(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Используйте: /show <дата>")
        return
    date = parts[1].strip()
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
    task = random.choice(RANDOM_TASKS)
    tasks.setdefault(date, []).append(task)
    bot.send_message(message.chat.id, f"Случайное место '{task}' добавлено на дату {date}.")

bot.polling(none_stop=True)