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

PLACES_INFO = {
    "Парк Горького": {
        "desc": "Центральный парк культуры и отдыха имени Горького — парк в Москве, расположенный на берегу Москвы-реки.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Gorky_Park_in_Moscow.jpg/800px-Gorky_Park_in_Moscow.jpg"
    },
    "ВДНХ": {
        "desc": "Выставка достижений народного хозяйства (ВДНХ) — крупнейшая выставка в России и одна из самых больших в мире.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/VDNH_in_Moscow.jpg/800px-VDNH_in_Moscow.jpg"
    },
    "Красная площадь": {
        "desc": "Красная площадь — центральная площадь Москвы, место проведения парадов и массовых мероприятий.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Red_Square_in_Moscow.jpg/800px-Red_Square_in_Moscow.jpg"
    },
    "Патриаршие пруды": {
        "desc": "Патриаршие пруды — пруды в центре Москвы, известные благодаря роману Михаила Булгакова 'Мастер и Маргарита'.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Patriarshy_Ponds_in_Moscow.jpg/800px-Patriarshy_Ponds_in_Moscow.jpg"
    },
    "Царицыно": {
        "desc": "Царицыно — музей-заповедник, расположенный в одноименном районе Москвы, известный своим дворцово-парковым ансамблем.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Tsaritsyno_in_Moscow.jpg/800px-Tsaritsyno_in_Moscow.jpg"
    },
    "Сокольники": {
        "desc": "Сокольники — парк в Москве, излюбленное место отдыха горожан, с обширной территорией и развитой инфраструктурой.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Sokolniki_Park_in_Moscow.jpg/800px-Sokolniki_Park_in_Moscow.jpg"
    },
    "Музеон": {
        "desc": "Музеон — парк искусств в Москве, где под открытым небом выставляются скульптуры и инсталляции современных художников.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Muzeon_Park_of_Arts_in_Moscow.jpg/800px-Muzeon_Park_of_Arts_in_Moscow.jpg"
    },
    "Парк Зарядье": {
        "desc": "Парк Зарядье — общественный парк в центре Москвы, расположенный рядом с Красной площадью.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Zaryadye_Park_in_Moscow.jpg/800px-Zaryadye_Park_in_Moscow.jpg"
    },
    "Воробьёвы горы": {
        "desc": "Воробьёвы горы — холмы в Москве, на которых расположены смотровые площадки с видом на город.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Vorobyovy_Gory_in_Moscow.jpg/800px-Vorobyovy_Gory_in_Moscow.jpg"
    },
    "Новодевичий пруд": {
        "desc": "Новодевичий пруд — пруд в Москве, расположенный рядом с Новодевичьим монастырём.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Novodevichy_Convent_and_Pond_in_Moscow.jpg/800px-Novodevichy_Convent_and_Pond_in_Moscow.jpg"
    },
    "Парк Победы": {
        "desc": "Парк Победы — парк в Москве, посвящённый памяти павших в Великой Отечественной войне.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Victory_Park_in_Moscow.jpg/800px-Victory_Park_in_Moscow.jpg"
    },
    "Аптекарский огород": {
        "desc": "Аптекарский огород — ботанический сад в Москве, один из старейших в России.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Aptekarsky_Ogorod_in_Moscow.jpg/800px-Aptekarsky_Ogorod_in_Moscow.jpg"
    },
    "Ботанический сад МГУ": {
        "desc": "Ботанический сад МГУ — ботанический сад Московского государственного университета.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/MSU_Botanical_Garden_in_Moscow.jpg/800px-MSU_Botanical_Garden_in_Moscow.jpg"
    },
    "Останкинский парк": {
        "desc": "Останкинский парк — парк в Москве, расположенный рядом с Останкинской телебашней.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Ostankino_Park_in_Moscow.jpg/800px-Ostankino_Park_in_Moscow.jpg"
    },
    "Парк Фили": {
        "desc": "Парк Фили — парк в Москве, расположенный на западе города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Filimonki_Park_in_Moscow.jpg/800px-Filimonki_Park_in_Moscow.jpg"
    },
    "Парк Кузьминки": {
        "desc": "Парк Кузьминки — парк в Москве, расположенный на юго-востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Kuzminki_Park_in_Moscow.jpg/800px-Kuzminki_Park_in_Moscow.jpg"
    },
    "Парк Северное Тушино": {
        "desc": "Парк Северное Тушино — парк в Москве, расположенный на севере города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Severnyye_Tushino_Park_in_Moscow.jpg/800px-Severnyye_Tushino_Park_in_Moscow.jpg"
    },
    "Парк Измайлово": {
        "desc": "Парк Измайлово — парк в Москве, расположенный на востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Izmaylovsky_Park_in_Moscow.jpg/800px-Izmaylovsky_Park_in_Moscow.jpg"
    },
    "Парк Лосиный остров": {
        "desc": "Парк Лосиный остров — парк в Москве, расположенный на западе города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Losiny_Ostrov_Park_in_Moscow.jpg/800px-Losiny_Ostrov_Park_in_Moscow.jpg"
    },
    "Парк Коломенское": {
        "desc": "Парк Коломенское — парк в Москве, расположенный на юге города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Kolomenskoye_Park_in_Moscow.jpg/800px-Kolomenskoye_Park_in_Moscow.jpg"
    },
    "Парк Садовники": {
        "desc": "Парк Садовники — парк в Москве, расположенный на юго-западе города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Sadovniki_Park_in_Moscow.jpg/800px-Sadovniki_Park_in_Moscow.jpg"
    },
    "Парк Бабушкинский": {
        "desc": "Парк Бабушкинский — парк в Москве, расположенный на востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Babushkinsky_Park_in_Moscow.jpg/800px-Babushkinsky_Park_in_Moscow.jpg"
    },
    "Парк Перловский": {
        "desc": "Парк Перловский — парк в Москве, расположенный на юго-востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Perlovsky_Park_in_Moscow.jpg/800px-Perlovsky_Park_in_Moscow.jpg"
    },
    "Парк Дружбы": {
        "desc": "Парк Дружбы — парк в Москве, расположенный на юго-западе города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Druzhby_Park_in_Moscow.jpg/800px-Druzhby_Park_in_Moscow.jpg"
    },
    "Парк Олимпийской деревни": {
        "desc": "Парк Олимпийской деревни — парк в Москве, расположенный на юге города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Olympic_Village_Park_in_Moscow.jpg/800px-Olympic_Village_Park_in_Moscow.jpg"
    },
    "Парк Тропарёво": {
        "desc": "Парк Тропарёво — парк в Москве, расположенный на юго-западе города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Troparevo_Park_in_Moscow.jpg/800px-Troparevo_Park_in_Moscow.jpg"
    },
    "Парк Школьный": {
        "desc": "Парк Школьный — парк в Москве, расположенный на северо-востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Shkolny_Park_in_Moscow.jpg/800px-Shkolny_Park_in_Moscow.jpg"
    },
    "Парк Лианозовский": {
        "desc": "Парк Лианозовский — парк в Москве, расположенный на северо-востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lianozovo_Park_in_Moscow.jpg/800px-Lianozovo_Park_in_Moscow.jpg"
    },
    "Парк Ангарские пруды": {
        "desc": "Парк Ангарские пруды — парк в Москве, расположенный на востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Angarskiye_Prudyi_Park_in_Moscow.jpg/800px-Angarskiye_Prudyi_Park_in_Moscow.jpg"
    },
    "Парк Яуза": {
        "desc": "Парк Яуза — парк в Москве, расположенный на северо-востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Yauza_Park_in_Moscow.jpg/800px-Yauza_Park_in_Moscow.jpg"
    },
    "Парк Митино": {
        "desc": "Парк Митино — парк в Москве, расположенный на северо-западе города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Mitino_Park_in_Moscow.jpg/800px-Mitino_Park_in_Moscow.jpg"
    },
    "Парк Сосенки": {
        "desc": "Парк Сосенки — парк в Москве, расположенный на юго-востоке города.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Sosenki_Park_in_Moscow.jpg/800px-Sosenki_Park_in_Moscow.jpg"
    },
    "Парк Малевича (Подмосковье)": {
        "desc": "Парк Малевича — парк в Подмосковье, посвящённый творчеству Казимира Малевича.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Malevich_Park_in_Podmoskovye.jpg/800px-Malevich_Park_in_Podmoskovye.jpg"
    },
    "Парк Мещерский (Подмосковье)": {
        "desc": "Парк Мещерский — парк в Подмосковье, расположенный в живописной местности.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Meshchersky_Park_in_Podmoskovye.jpg/800px-Meshchersky_Park_in_Podmoskovye.jpg"
    },
    "Парк Валуевский (Подмосковье)": {
        "desc": "Парк Валуевский — парк в Подмосковье, известный своими природными ландшафтами.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Valuyevskiy_Park_in_Podmoskovye.jpg/800px-Valuyevskiy_Park_in_Podmoskovye.jpg"
    },
    "Парк Середниково (Подмосковье)": {
        "desc": "Парк Середниково — парк в Подмосковье, популярное место для семейного отдыха.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Serebryanyye_Pruady_Park_in_Podmoskovye.jpg/800px-Serebryanyye_Pruady_Park_in_Podmoskovye.jpg"
    },
    "Парк Архангельское (Подмосковье)": {
        "desc": "Парк Архангельское — парк в Подмосковье, известный своим архитектурным ансамблем.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Arkhangelskoye_Park_in_Podmoskovye.jpg/800px-Arkhangelskoye_Park_in_Podmoskovye.jpg"
    },
    "Парк Абрамцево (Подмосковье)": {
        "desc": "Парк Абрамцево — парк в Подмосковье, известный своими историческими памятниками.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Abramtsevo_Park_in_Podmoskovye.jpg/800px-Abramtsevo_Park_in_Podmoskovye.jpg"
    },
    "Парк Звенигород (Подмосковье)": {
        "desc": "Парк Звенигород — парк в Подмосковье, расположенный в живописной местности.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Zvenigorod_Park_in_Podmoskovye.jpg/800px-Zvenigorod_Park_in_Podmoskovye.jpg"
    },
    "Парк Лесная сказка (Подмосковье)": {
        "desc": "Парк Лесная сказка — парк в Подмосковье, популярное место для отдыха на природе.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Lesnaya_Skazka_Park_in_Podmoskovye.jpg/800px-Lesnaya_Skazka_Park_in_Podmoskovye.jpg"
    },
    "Парк Пехорка (Подмосковье)": {
        "desc": "Парк Пехорка — парк в Подмосковье, известный своими природными ландшафтами.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Pejorka_Park_in_Podmoskovye.jpg/800px-Pejorka_Park_in_Podmoskovye.jpg"
    },
    "Парк Радуга (Подмосковье)": {
        "desc": "Парк Радуга — парк в Подмосковье, популярное место для семейного отдыха.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Raduga_Park_in_Podmoskovye.jpg/800px-Raduga_Park_in_Podmoskovye.jpg"
    },
    "Парк Дубрава (Подмосковье)": {
        "desc": "Парк Дубрава — парк в Подмосковье, известный своими историческими памятниками.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Dubravka_Park_in_Podmoskovye.jpg/800px-Dubravka_Park_in_Podmoskovye.jpg"
    },
    "Парк Воскресенское (Подмосковье)": {
        "desc": "Парк Воскресенское — парк в Подмосковье, расположенный в живописной местности.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Voskresenskoye_Park_in_Podmoskovye.jpg/800px-Voskresenskoye_Park_in_Podmoskovye.jpg"
    },
    "Парк Лосиный остров (Подмосковье)": {
        "desc": "Парк Лосиный остров — парк в Подмосковье, известный своими природными ландшафтами.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Losiny_Ostrov_Park_in_Podmoskovye.jpg/800px-Losiny_Ostrov_Park_in_Podmoskovye.jpg"
    },
    "Парк Солнечная поляна (Подмосковье)": {
        "desc": "Парк Солнечная поляна — парк в Подмосковье, популярное место для отдыха на природе.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Solnechnaya_Polyana_Park_in_Podmoskovye.jpg/800px-Solnechnaya_Polyana_Park_in_Podmoskovye.jpg"
    },
    "Парк Сказка (Подмосковье)": {
        "desc": "Парк Сказка — парк в Подмосковье, известный своими сказочными пейзажами.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Skazka_Park_in_Podmoskovye.jpg/800px-Skazka_Park_in_Podmoskovye.jpg"
    },
    "Парк Кусково": {
        "desc": "Кусково — усадьба XVIII века с парком и музеем в Москве.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Kuskovo_Estate_in_Moscow.jpg/800px-Kuskovo_Estate_in_Moscow.jpg"
    },
    "Парк Раменки": {
        "desc": "Раменки — район на западе Москвы, известный своими парками и природными зонами.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Ramenki_in_Moscow.jpg/800px-Ramenki_in_Moscow.jpg"
    },
    "Парк Тушино": {
        "desc": "Тушино — район на севере Москвы, расположенный вдоль реки Москвы.",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Tushino_in_Moscow.jpg/800px-Tushino_in_Moscow.jpg"
    }
}

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
    save_tasks()
    # Если задача совпадает с местом из PLACES_INFO — отправить фото и описание
    if task in PLACES_INFO:
        info = PLACES_INFO[task]
        bot.send_photo(message.chat.id, info["photo"], caption=f"{task}\n{info['desc']}")
    else:
        bot.send_message(message.chat.id, f"Задача '{task}' добавлена на дату {date}.")

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
    place = random.choice(list(PLACES_INFO.keys()))
    info = PLACES_INFO[place]
    user_tasks.setdefault(date, []).append({"text": place, "done": False})
    bot.send_photo(message.chat.id, info["photo"], caption=f"{place}\n{info['desc']}")
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

