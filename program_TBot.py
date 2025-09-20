import telebot
import random
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные окружения из файла .env

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен Telegram-бота не найден! Установите переменную окружения TELEGRAM_BOT_TOKEN.")
bot = telebot.TeleBot(TOKEN)

HELP = (
    "/start - Приветствие\n"
    "/help - Напечатать справку по программе.\n"
    "/add <дата> <задача> - Добавить задачу на дату.\n"
    "/show <дата> [страница] - Показать задачи на дату (по страницам).\n"
    "/showall [страница] - Показать все задачи (по страницам).\n"
    "/random <дата> - Добавить случайное место на дату.\n"
    "/delete <дата> <номер_задачи> - Удалить задачу.\n"
    "/edit <дата> <номер_задачи> <новый_текст> - Редактировать задачу.\n"
    "/done <дата> <номер_задачи> - Отметить задачу выполненной.\n"
    "/find <текст> - Поиск задач по тексту.\n"
    "/stats - Статистика задач.\n"
    "/export - Экспорт всех задач в файл.\n"
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
PAGE_SIZE = 10

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

def get_user_tasks(user_id):
    return tasks.setdefault(str(user_id), {})

def is_valid_date(date):
    return re.match(r"\d{2}\.\d{2}(\.\d{4})?$", date) is not None

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот-планировщик. Введите /help для списка команд.")

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
    user_tasks = get_user_tasks(message.from_user.id)
    user_tasks.setdefault(date, []).append({"text": task, "done": False})
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена на дату {date}.")
    save_tasks()

def format_tasks(task_list, page=1):
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    result = ""
    for i, task in enumerate(task_list[start:end], start=start + 1):
        status = "✅" if task.get("done") else "❌"
        result += f"{i}. {status} {task['text']}\n"
    return result if result else "Нет задач на этой странице."

@bot.message_handler(commands=["show"])
def show_tasks(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Используйте: /show <дата> [страница]")
        return
    date = parts[1].strip()
    page = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1
    if not is_valid_date(date):
        bot.send_message(message.chat.id, "Дата должна быть в формате ДД.ММ или ДД.ММ.ГГГГ")
        return
    user_tasks = get_user_tasks(message.from_user.id)
    if date in user_tasks and user_tasks[date]:
        text = f"{date.upper()} (стр. {page}):\n"
        text += format_tasks(user_tasks[date], page)
    else:
        text = "Задач на эту дату нет."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["showall"])
def show_all_tasks(message):
    parts = message.text.split()
    page = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
    user_tasks = get_user_tasks(message.from_user.id)
    all_tasks = []
    for date, task_list in user_tasks.items():
        for task in task_list:
            all_tasks.append({"date": date, "text": task["text"], "done": task.get("done", False)})
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    text = ""
    for i, task in enumerate(all_tasks[start:end], start=start + 1):
        status = "✅" if task["done"] else "❌"
        text += f"{i}. [{task['date']}] {status} {task['text']}\n"
    if not text:
        text = "Нет задач на этой странице."
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
    user_tasks = get_user_tasks(message.from_user.id)
    task = random.choice(RANDOM_TASKS)
    user_tasks.setdefault(date, []).append({"text": task, "done": False})
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
        user_tasks = get_user_tasks(message.from_user.id)
        if date in user_tasks and 0 <= idx < len(user_tasks[date]):
            removed = user_tasks[date].pop(idx)
            save_tasks()
            bot.send_message(message.chat.id, f"Задача '{removed['text']}' удалена с даты {date}.")
        else:
            bot.send_message(message.chat.id, "Неверная дата или номер задачи.")
    except ValueError:
        bot.send_message(message.chat.id, "Номер задачи должен быть числом.")

@bot.message_handler(commands=["edit"])
def edit_task(message):
    parts = message.text.split(maxsplit=3)
    if len(parts) < 4:
        bot.send_message(message.chat.id, "Используйте: /edit <дата> <номер_задачи> <новый_текст>")
        return
    date = parts[1].strip()
    try:
        idx = int(parts[2].strip()) - 1
        new_text = parts[3].strip()
        user_tasks = get_user_tasks(message.from_user.id)
        if date in user_tasks and 0 <= idx < len(user_tasks[date]):
            user_tasks[date][idx]["text"] = new_text
            save_tasks()
            bot.send_message(message.chat.id, f"Задача на {date} №{idx+1} изменена.")
        else:
            bot.send_message(message.chat.id, "Неверная дата или номер задачи.")
    except ValueError:
        bot.send_message(message.chat.id, "Номер задачи должен быть числом.")

@bot.message_handler(commands=["done"])
def done_task(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(message.chat.id, "Используйте: /done <дата> <номер_задачи>")
        return
    date = parts[1].strip()
    try:
        idx = int(parts[2].strip()) - 1
        user_tasks = get_user_tasks(message.from_user.id)
        if date in user_tasks and 0 <= idx < len(user_tasks[date]):
            user_tasks[date][idx]["done"] = True
            save_tasks()
            bot.send_message(message.chat.id, f"Задача на {date} №{idx+1} отмечена как выполненная.")
        else:
            bot.send_message(message.chat.id, "Неверная дата или номер задачи.")
    except ValueError:
        bot.send_message(message.chat.id, "Номер задачи должен быть числом.")

@bot.message_handler(commands=["find"])
def find_task(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Используйте: /find <текст>")
        return
    query = parts[1].strip().lower()
    user_tasks = get_user_tasks(message.from_user.id)
    found = []
    for date, task_list in user_tasks.items():
        for i, task in enumerate(task_list, start=1):
            if query in task["text"].lower():
                status = "✅" if task.get("done") else "❌"
                found.append(f"{date} {i}. {status} {task['text']}")
    if found:
        bot.send_message(message.chat.id, "\n".join(found))
    else:
        bot.send_message(message.chat.id, "Задачи не найдены.")

@bot.message_handler(commands=["stats"])
def stats(message):
    user_tasks = get_user_tasks(message.from_user.id)
    total = sum(len(task_list) for task_list in user_tasks.values())
    done = sum(task.get("done") for task_list in user_tasks.values() for task in task_list)
    bot.send_message(message.chat.id, f"Всего задач: {total}\nВыполнено: {done}\nОсталось: {total - done}")

@bot.message_handler(commands=["export"])
def export_tasks(message):
    user_tasks = get_user_tasks(message.from_user.id)
    lines = []
    for date, task_list in user_tasks.items():
        for i, task in enumerate(task_list, start=1):
            status = "✅" if task.get("done") else "❌"
            lines.append(f"{date} {i}. {status} {task['text']}")
    if lines:
        filename = f"tasks_{message.from_user.id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        with open(filename, "rb") as f:
            bot.send_document(message.chat.id, f)
        os.remove(filename)
    else:
        bot.send_message(message.chat.id, "Нет задач для экспорта.")

bot.polling(none_stop=True)