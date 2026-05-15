import streamlit as st
import random
import json
import os
from datetime import datetime

st.set_page_config(
    page_title=" IT Викторина",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LEADERBOARD_FILE = "leaderboard.json"


def load_leaderboard():

    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_leaderboard(leaderboard):

    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)


def clear_leaderboard():

    if os.path.exists(LEADERBOARD_FILE):
        os.remove(LEADERBOARD_FILE)



def add_score_to_leaderboard(name, score, total_possible, difficulty, percentage):
    leaderboard = load_leaderboard()

    found = False
    for entry in leaderboard:
        if entry["name"] == name:

            if score > entry["score"]:
                entry["score"] = score
                entry["total_possible"] = total_possible
                entry["difficulty"] = difficulty
                entry["percentage"] = percentage
                entry["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            found = True
            break

    if not found:
        leaderboard.append({
            "name": name,
            "score": score,
            "total_possible": total_possible,
            "difficulty": difficulty,
            "percentage": percentage,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:20]
    save_leaderboard(leaderboard)



st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
        color: #ffffff !important;
    }

    .stRadio label p {
        color: #ffffff !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.4); }
        70% { box-shadow: 0 0 0 20px rgba(0, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0); }
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    @keyframes titleGlow {
        0% { text-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88; }
        50% { text-shadow: 0 0 20px #00ff88, 0 0 30px #00b4ff; }
        100% { text-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88; }
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ff88, #00b4ff, #667eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        animation: titleGlow 2s ease-in-out infinite;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #aaa;
        margin-bottom: 30px;
    }

    .subtitle span {
        background: rgba(0, 255, 255, 0.1);
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
    }

    .question-text {
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00b4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
        line-height: 1.3;
    }

    .option-btn {
        padding: 12px 20px;
        margin: 8px 0;
        border-radius: 12px;
        background: rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }

    .score-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px 20px;
        border-radius: 50px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .correct-answer {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        padding: 20px;
        border-radius: 15px;
        animation: glowPulse 1.5s infinite;
    }

    .wrong-answer {
        background: linear-gradient(135deg, #cb2d3e, #ef473a);
        padding: 20px;
        border-radius: 15px;
    }

    .progress-bar {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
    }

    .progress-fill {
        background: linear-gradient(90deg, #00ff88, #00b4ff);
        height: 100%;
        transition: width 0.5s ease;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: bold;
        transition: transform 0.2s;
    }

    .stButton > button:hover {
        transform: scale(1.05);
    }

    .stRadio > div {
        gap: 12px;
    }

    .stRadio label {
        background: rgba(255,255,255,0.05);
        padding: 12px 18px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s;
    }

    .stRadio label:hover {
        background: rgba(0, 255, 255, 0.15);
        border-color: #00ffff;
    }

    .difficulty-card {
        background: rgba(0,0,0,0.6);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid transparent;
    }

    .difficulty-card:hover {
        transform: translateY(-5px);
        border-color: #00ffff;
    }

    .easy {
        border-left: 5px solid #00ff88;
    }

    .medium {
        border-left: 5px solid #ffaa00;
    }

    .hard {
        border-left: 5px solid #ff4444;
    }

    
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center;">
    <h1 class="main-title" style="font-size: 4.5rem;">⚡ CODE BATTLE ⚡</h1>
    <div class="subtitle">
        <span> IT-ВИКТОРИНА | ПРОВЕРЬ СВОИ ЗНАНИЯ </span>
    </div>
</div>
""", unsafe_allow_html=True)
# вопросы
questions_db = {
    "easy": [
        {"question": "Какой функцией в Python выводят текст на консоль?",
         "options": ["console.log()", "print()", "echo()", "write()"], "correct": "print()",
         "explanation": "print() — основная функция вывода в Python."},
        {"question": "Какой символ используется для комментария в Python?",
         "options": ["//", "#", "/*", "--"], "correct": "#",
         "explanation": "# — всё после него до конца строки игнорируется."},
        {"question": "Какой тип данных у переменной x = 42?",
         "options": ["<class 'float'>", "<class 'int'>", "<class 'str'>", "<class 'bool'>"], "correct": "<class 'int'>",
         "explanation": "42 — целое число, тип int."},
        {"question": "Какой оператор проверяет равенство в Python?",
         "options": ["=", "==", "===", "!="], "correct": "==",
         "explanation": "== сравнивает значения, = — присваивание."},
        {"question": "Как создать список в Python?",
         "options": ["{1,2,3}", "(1,2,3)", "[1,2,3]", "<1,2,3>"], "correct": "[1,2,3]",
         "explanation": "Квадратные скобки создают список list."},
        {"question": "Что выведет type(3.14)?",
         "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"],
         "correct": "<class 'float'>",
         "explanation": "Числа с точкой — тип float."},
        {"question": "Как получить длину строки s = 'Hello'?",
         "options": ["s.length()", "len(s)", "s.len()", "length(s)"], "correct": "len(s)",
         "explanation": "len() — встроенная функция для длины."},
        {"question": "Какой оператор используется для возведения в степень?",
         "options": ["^", "**", "pow", "&"], "correct": "**",
         "explanation": "** — оператор степени: 2**3 = 8."},
        {"question": "Что делает функция input()?",
         "options": ["Выводит текст", "Считывает ввод с клавиатуры", "Открывает файл", "Завершает программу"],
         "correct": "Считывает ввод с клавиатуры",
         "explanation": "input() ждёт ввод от пользователя и ВСЕГДА возвращает строку (str)."},
        {"question": "Какой результат int(3.99)?",
         "options": ["3.99", "4", "3", "Ошибка"], "correct": "3",
         "explanation": "int() отбрасывает дробную часть (округление вниз)."},
        {"question": "Как проверить чётность числа x?",
         "options": ["x % 2 == 0", "x / 2 == 0", "x // 2 == 0", "x % 2 != 0"], "correct": "x % 2 == 0",
         "explanation": "Остаток от деления на 2 равен 0 у чётных чисел."},
        {"question": "Как создать словарь (dict)?",
         "options": ["[1,2,3]", "{'a':1, 'b':2}", "(1,2,3)", "{1,2,3}"], "correct": "{'a':1, 'b':2}",
         "explanation": "Словарь — пары ключ:значение в фигурных скобках."},
        {"question": "Какой результат 5 // 2?",
         "options": ["2.5", "2", "3", "2.0"], "correct": "2",
         "explanation": "// — целочисленное деление (деление нацело)."},
        {"question": "Как объявить переменную name со значением 'Анна'?",
         "options": ["name = 'Анна'", "var name = 'Анна'", "name := 'Анна'", "string name = 'Анна'"],
         "correct": "name = 'Анна'",
         "explanation": "В Python переменные объявляются без ключевых слов."},
        {"question": "Что вернёт range(5) в Python 3?",
         "options": ["[0,1,2,3,4]", "объект range(0, 5)", "(0,1,2,3,4)", "{0,1,2,3,4}"],
         "correct": "объект range(0, 5)",
         "explanation": "range() возвращает итерируемый объект, а не список. Для получения списка используйте list(range(5))."},
        {"question": "Какой оператор 'И' в Python?",
         "options": ["&", "and", "&&", "or"], "correct": "and",
         "explanation": "and — логическое И в Python."},
        {"question": "Какой тип данных у True?",
         "options": ["<class 'int'>", "<class 'bool'>", "<class 'str'>", "<class 'float'>"],
         "correct": "<class 'bool'>",
         "explanation": "True и False — булевый тип bool (наследник int)."},
        {"question": "Как добавить элемент в конец списка lst?",
         "options": ["lst.add(5)", "lst.append(5)", "lst.insert(5)", "lst.push(5)"], "correct": "lst.append(5)",
         "explanation": ".append() добавляет элемент в конец списка."},
        {"question": "Что выведет print(type(None))?",
         "options": ["<class 'None'>", "<class 'NoneType'>", "None", "Ошибка"], "correct": "<class 'NoneType'>",
         "explanation": "None имеет тип NoneType."},
        {"question": "Как преобразовать строку '123' в число?",
         "options": ["str(123)", "int('123')", "float('123')", "'123'.toInt()"], "correct": "int('123')",
         "explanation": "int() преобразует строку в целое число."}
    ],
    "medium": [
        {"question": "Что выведет код: lst = [1,2,3]; print(lst[::-1])?",
         "options": ["[1,2,3]", "[3,2,1]", "[]", "None"], "correct": "[3,2,1]",
         "explanation": "[::-1] — разворот списка (срез с шагом -1)."},
        {"question": "Что такое рекурсия?",
         "options": ["Цикл с условием", "Функция, вызывающая себя", "Тип данных", "Библиотека"],
         "correct": "Функция, вызывающая себя",
         "explanation": "Рекурсия — когда функция вызывает саму себя."},
        {"question": "Что выведет код: x = [1,2,3]; y = x; y.append(4); print(x)?",
         "options": ["[1,2,3]", "[1,2,3,4]", "Ошибка", "[4]"], "correct": "[1,2,3,4]",
         "explanation": "Списки мутабельны. y = x — ссылка на тот же объект."},
        {"question": "Какой фреймворк НЕ является бэкенд-фреймворком Python?",
         "options": ["Django", "React", "Flask", "FastAPI"], "correct": "React",
         "explanation": "React — фронтенд-библиотека JavaScript."},
        {"question": "Что выведет код: list(map(int, ['1','2','3']))?",
         "options": ["['1','2','3']", "[1,2,3]", "Ошибка", "['1','2','3','int']"], "correct": "[1,2,3]",
         "explanation": "map применяет int к каждому элементу, list() преобразует результат в список."},
        {"question": "Что такое декоратор в Python?",
         "options": ["Класс для оформления", "Функция, изменяющая поведение другой функции", "Тип переменной",
                     "Математическая операция"],
         "correct": "Функция, изменяющая поведение другой функции",
         "explanation": "Декораторы оборачивают одну функцию другой."},
        {"question": "Что выведет код: print(0.1 + 0.2 == 0.3)?",
         "options": ["True", "False", "None", "Ошибка"], "correct": "False",
         "explanation": "0.1 + 0.2 = 0.30000000000000004 из-за погрешности float."},
        {"question": "Какой метод удаляет последний элемент списка?",
         "options": ["pop()", "remove()", "delete()", "clear()"], "correct": "pop()",
         "explanation": "pop() удаляет последний элемент и возвращает его."},
        {"question": "Что такое *args в функции?",
         "options": ["Кортеж аргументов", "Словарь аргументов", "Список аргументов", "Множество аргументов"],
         "correct": "Кортеж аргументов",
         "explanation": "*args собирает лишние позиционные аргументы в кортеж."},
        {"question": "Что выведет код: [x**2 for x in range(5)]?",
         "options": ["[0,1,4,9,16]", "[1,4,9,16,25]", "[0,1,2,3,4]", "Ошибка"], "correct": "[0,1,4,9,16]",
         "explanation": "Генератор списка возводит числа от 0 до 4 в квадрат."},
        {"question": "Что выведет код: print(2 ** 3 ** 2)?",
         "options": ["64", "512", "36", "Ошибка"], "correct": "512",
         "explanation": "** имеет правую ассоциативность: 3**2=9, 2**9=512."},
        {"question": "Какой оператор проверяет наличие элемента в коллекции?",
         "options": ["in", "has", "contains", "exists"], "correct": "in",
         "explanation": "'in' проверяет вхождение элемента."},
        {"question": "Что такое try/except?",
         "options": ["Цикл", "Условный оператор", "Обработка исключений", "Функция"], "correct": "Обработка исключений",
         "explanation": "try/except ловит и обрабатывает ошибки."},
        {"question": "Что выведет код: set([1,2,2,3,3,3])?",
         "options": ["[1,2,3]", "{1,2,3}", "(1,2,3)", "{1:2,3:3}"], "correct": "{1,2,3}",
         "explanation": "set() оставляет только уникальные элементы."},
        {"question": "Как объявить класс в Python?",
         "options": ["class MyClass:", "def MyClass:", "object MyClass:", "new MyClass:"], "correct": "class MyClass:",
         "explanation": "class — ключевое слово для создания класса."},
        {"question": "Что такое метод __init__?",
         "options": ["Деструктор", "Конструктор", "Магический метод сравнения", "Метод вывода"],
         "correct": "Конструктор",
         "explanation": "__init__ вызывается при создании объекта."},
        {"question": "Как получить все ключи словаря d?",
         "options": ["d.keys()", "d.values()", "d.items()", "d.get()"], "correct": "d.keys()",
         "explanation": "d.keys() возвращает все ключи словаря."},
        {"question": "Что выведет код: print(True + True + False)?",
         "options": ["2", "1", "True", "Ошибка"], "correct": "2",
         "explanation": "True=1, False=0, поэтому 1+1+0=2."},
        {"question": "Как создать независимую копию списка lst?",
         "options": ["new_lst = lst", "new_lst = lst[:]", "new_lst = list.copy(lst)", "new_lst = append(lst)"],
         "correct": "new_lst = lst[:]",
         "explanation": "Срез [:] создает новый объект списка."},
        {"question": "Что такое GIL в Python?",
         "options": ["Глобальная библиотека", "Глобальная блокировка интерпретатора", "Графический интерфейс",
                     "Генератор исключений"],
         "correct": "Глобальная блокировка интерпретатора",
         "explanation": "GIL ограничивает параллельное выполнение потоков в CPython."}
    ],
    "hard": [
        {"question": "Что выведет данный код? def f(x, lst=[]): lst.append(x); return lst; print(f(1)); print(f(2))",
         "options": ["[1] [2]", "[1] [1,2]", "[1,1] [2,2]", "Ошибка"], "correct": "[1] [1,2]",
         "explanation": "Параметр по умолчанию создаётся один раз при определении функции и используется при всех вызовах."},
        {"question": "Какой баг уничтожил ракету Ariane 5 в 1996 году?",
         "options": ["Переполнение целого числа", "Деление на ноль", "Бесконечный цикл", "Утечка памяти"],
         "correct": "Переполнение целого числа",
         "explanation": "64-битное число преобразовали в 16-битное → переполнение → ракета самоуничтожилась."},
        {"question": "Чем отличается оператор is от == в Python?",
         "options": ["is сравнивает значения, == сравнивает типы", "is сравнивает идентичность объектов, == сравнивает значения",
                     "is сравнивает типы, == сравнивает значения", "Это одно и то же"], "correct": "is сравнивает идентичность объектов, == сравнивает значения",
         "explanation": "is проверяет, ссылаются ли переменные на один объект в памяти, == сравнивает значения."},
        {"question": "Что выведет код: print(not (False or True) and False)?",
         "options": ["True", "False", "None", "Ошибка"], "correct": "False",
         "explanation": "False or True = True, not True = False, False and False = False."},
        {"question": "Что такое метакласс в Python?",
         "options": ["Класс, который создаёт другие классы", "Абстрактный класс", "Декоратор класса", "Вложенный класс"],
         "correct": "Класс, который создаёт другие классы",
         "explanation": "Метакласс — это класс, который создаёт другие классы (например, type)."},
        {"question": "Что выведет код: print(float('inf') > 10**1000)?",
         "options": ["True", "False", "None", "Ошибка"], "correct": "True",
         "explanation": "inf — бесконечность, больше любого числа."},
        {"question": "Что делает декоратор @property в Python?",
         "options": ["Позволяет обращаться к методу как к атрибуту", "Делает метод статическим", "Создаёт приватный метод", "Кэширует результат метода"],
         "correct": "Позволяет обращаться к методу как к атрибуту",
         "explanation": "@property позволяет обращаться к методу как к атрибуту без вызова."},
        {"question": "Что выведет код: print(1_000_000)?",
         "options": ["Ошибка", "1000000", "1000", "1 000 000"], "correct": "1000000",
         "explanation": "Подчёркивания в числах игнорируются, это для удобства чтения."},
        {"question": "Что такое слайс (срез) с шагом?",
         "options": ["[start:stop:step]", "[start:step:stop]", "(start:stop:step)", "[start,stop,step]"],
         "correct": "[start:stop:step]",
         "explanation": "Пример: [1,2,3,4,5][::2] → [1,3,5]."},
        {"question": "Как создать кортеж с одним элементом?",
         "options": ["(5)", "5,", "[5]", "{5}"], "correct": "5,",
         "explanation": "Кортеж из одного элемента: (5,) или просто 5, (запятая обязательна)."},
        {"question": "Что такое __slots__ в Python?",
         "options": ["Оптимизация памяти для атрибутов", "Слоты для методов", "Список аргументов", "Тип данных"],
         "correct": "Оптимизация памяти для атрибутов",
         "explanation": "__slots__ ограничивает атрибуты и экономит память."},
        {"question": "Что выведет код: print(all([True, False, True]))?",
         "options": ["True", "False", "None", "Ошибка"], "correct": "False",
         "explanation": "all() возвращает True только если все элементы True."},
        {"question": "Что делает functools.lru_cache?",
         "options": ["Кэширует результаты вызовов функций", "Логирует вызовы функций", "Профилирует код", "Работает с файлами"],
         "correct": "Кэширует результаты вызовов функций",
         "explanation": "lru_cache запоминает результаты вызовов для ускорения повторных вызовов."},
        {"question": "Что произойдёт при повторном импорте модуля? import module во второй раз",
         "options": ["Ошибка импорта", "Модуль загружается заново", "Модуль берётся из кэша", "Программа зависает"],
         "correct": "Модуль берётся из кэша",
         "explanation": "Python кэширует импортированные модули в sys.modules."},
        {"question": "Что выведет код: print((lambda x: x**2)(5))?",
         "options": ["5", "10", "25", "Ошибка"], "correct": "25",
         "explanation": "Лямбда-функция: lambda x: x**2 — квадрат числа."},
        {"question": "Какой алгоритм сортировки использует Python по умолчанию?",
         "options": ["Быстрая сортировка", "Timsort", "Сортировка слиянием", "Пузырьковая"], "correct": "Timsort",
         "explanation": "Timsort — гибрид сортировки слиянием и вставками."},
        {"question": "Что такое async/await в Python?",
         "options": ["Асинхронное программирование", "Многопоточность", "Многопроцессорность", "Обработка сигналов"],
         "correct": "Асинхронное программирование",
         "explanation": "async/await — синтаксис для асинхронного кода."},
        {"question": "Что выведет код: print(bytearray(b'Hello')[0])?",
         "options": ["72", "H", "72.0", "Ошибка"], "correct": "72",
         "explanation": "bytearray возвращает числа (коды символов). Буква 'H' имеет ASCII код 72."},
        {"question": "Что выведет код: print(bool([]), bool([0]))?",
         "options": ["True, True", "False, True", "False, False", "True, False"], "correct": "False, True",
         "explanation": "Пустые коллекции в Python приводятся к False, а непустые (даже с нулем) — к True."},
        {"question": "Что выведет код: print(0 == False and 1 == True)?",
         "options": ["True", "False", "None", "Ошибка"], "correct": "True",
         "explanation": "0 == False → True, 1 == True → True, True and True → True."}
    ]
}

POINTS_MULTIPLIER = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}


def show_partners():

    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("mindpro_logo.png", width=200)
    with col2:
        st.image("ktelecom_logo.png", width=200)


if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'correct_count' not in st.session_state:  # количество правильных ответов
    st.session_state.correct_count = 0
if 'score' not in st.session_state:  # общее количество очков
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = None
if 'selected_opt' not in st.session_state:
    st.session_state.selected_opt = None
if 'finished' not in st.session_state:
    st.session_state.finished = False
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""
if 'score_saved' not in st.session_state:
    st.session_state.score_saved = False


def start_quiz(difficulty):
    st.session_state.difficulty = difficulty
    st.session_state.questions = questions_db[difficulty].copy()
    random.shuffle(st.session_state.questions)
    st.session_state.current_q = 0
    st.session_state.correct_count = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.show_feedback = None
    st.session_state.selected_opt = None
    st.session_state.finished = False
    st.session_state.score_saved = False


def check_answer():
    if st.session_state.selected_opt is None:
        st.toast(" Выбери вариант ответа!")
        return
    current = st.session_state.questions[st.session_state.current_q]
    multiplier = POINTS_MULTIPLIER[st.session_state.difficulty]

    if st.session_state.selected_opt == current["correct"]:
        st.session_state.correct_count += 1
        st.session_state.score += multiplier
        st.session_state.show_feedback = "correct"
    else:
        st.session_state.show_feedback = "wrong"
    st.session_state.answered = True

def next_q():
    if st.session_state.current_q < len(st.session_state.questions) - 1:
        st.session_state.current_q += 1
        st.session_state.answered = False
        st.session_state.show_feedback = None
        st.session_state.selected_opt = None
    else:
        st.session_state.finished = True


def restart():
    st.session_state.difficulty = None
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.correct_count = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.show_feedback = None
    st.session_state.selected_opt = None
    st.session_state.finished = False
    st.session_state.score_saved = False



st.markdown("---")

if st.session_state.difficulty is None and not st.session_state.finished:


    if st.session_state.player_name == "":
        st.markdown("###  Введите ваше имя")
        col_name1, col_name2, col_name3 = st.columns([1, 2, 1])
        with col_name2:
            player_name_input = st.text_input("", placeholder="Например: Stiv", key="name_input",
                                              label_visibility="collapsed")
            if player_name_input:
                if len(player_name_input.strip()) >= 2:
                    st.session_state.player_name = player_name_input.strip()
                    st.rerun()
                else:
                    st.error(" Имя должно содержать минимум 2 символа!")
        st.markdown("---")


    if st.session_state.player_name:
        st.markdown("# ВЫБЕРИ РЕЖИМ ИГРЫ")
        st.markdown(f"### Привет, **{st.session_state.player_name}**! Выбери уровень сложности:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="difficulty-card easy" style="text-align:center;">
                <i class="fas fa-seedling" style="font-size: 6rem; color: #00ff88;"></i>
                <h2 style="color:#00ff88;">ЛЁГКИЙ</h2>
                <p>Для начинающих<br>Базовые вопросы</p>
                <p style="font-size:0.8rem;">20 вопросов | x1 очко</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(" СТАРТ", key="start_easy", use_container_width=True):
                start_quiz("easy")
                st.rerun()

        with col2:
            st.markdown("""
            <div class="difficulty-card medium" style="text-align:center;">
                <i class="fas fa-bolt" style="font-size: 6rem; color: #ffaa00;"></i>
                <h2 style="color:#ffaa00;">СРЕДНИЙ</h2>
                <p>Знаешь основы<br>Логические задачи</p>
                <p style="font-size:0.8rem;">20 вопросов | x2 очка</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(" СТАРТ", key="start_medium", use_container_width=True):
                start_quiz("medium")
                st.rerun()

        with col3:
            st.markdown("""
            <div class="difficulty-card hard" style="text-align:center;">
                <i class="fas fa-fire" style="font-size: 6rem; color: #ff4444;"></i>
                <h2 style="color:#ff4444;">СЛОЖНЫЙ</h2>
                <p>Сложные вопросы<br>Для опытных разработчиков</p>
                <p style="font-size:0.8rem;">20 вопросов | x3 очка</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(" СТАРТ", key="start_hard", use_container_width=True):
                start_quiz("hard")
                st.rerun()

        st.markdown("---")
        st.info("💡 Совет: Начинай с лёгкого, чтобы разогреться! Чем сложнее уровень, тем больше множитель очков.")


elif st.session_state.difficulty is not None and not st.session_state.finished:
    current_q = st.session_state.questions[st.session_state.current_q]

    diff_icons = {"easy": " ЛЁГКИЙ", "medium": " СРЕДНИЙ", "hard": " СЛОЖНЫЙ"}
    diff_colors = {"easy": "#00ff88", "medium": "#ffaa00", "hard": "#ff4444"}

    st.markdown(
        f"<p style='text-align:center; color:{diff_colors[st.session_state.difficulty]}; font-weight:bold;'>{diff_icons[st.session_state.difficulty]}</p>",
        unsafe_allow_html=True)

    # прогресс-бар
    progress_pct = (st.session_state.current_q) / len(st.session_state.questions)
    max_possible_for_current = len(st.session_state.questions) * POINTS_MULTIPLIER[st.session_state.difficulty]
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_pct * 100}%"></div>
    </div>
    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
        <span> Вопрос {st.session_state.current_q + 1}/{len(st.session_state.questions)}</span>
        <span class="score-badge"> {st.session_state.score} очков (x{POINTS_MULTIPLIER[st.session_state.difficulty]})</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{current_q["question"]}</div>', unsafe_allow_html=True)

    selected = st.radio(
        "**Выбери ответ:**",
        current_q["options"],
        key=f"q_{st.session_state.current_q}",
        disabled=st.session_state.answered,
        index=None,
        label_visibility="collapsed"
    )

    if selected:
        st.session_state.selected_opt = selected

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.answered:
            if st.button("ПРОВЕРИТЬ ОТВЕТ", use_container_width=True):
                check_answer()
                st.rerun()

    if st.session_state.show_feedback:
        if st.session_state.show_feedback == "correct":
            st.markdown(f"""
            <div class="correct-answer">
                <h3> ВЕРНО!</h3>
                <p><strong>Правильный ответ:</strong> {current_q['correct']}</p>
                <p><em>{current_q['explanation']}</em></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="wrong-answer">
                <h3> НЕВЕРНО</h3>
                <p><strong>Правильный ответ:</strong> {current_q['correct']}</p>
                <p><em>{current_q['explanation']}</em></p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("СЛЕДУЮЩИЙ ВОПРОС", use_container_width=True):
            next_q()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# финал
elif st.session_state.finished:
    max_possible_score = len(st.session_state.questions) * POINTS_MULTIPLIER[st.session_state.difficulty]
    percentage = (st.session_state.score / max_possible_score) * 100

    st.markdown(f"""
    <div class="quiz-card" style="text-align:center;">
        <h1>ИТОГИ ВИКТОРИНЫ</h1>
        <div style="font-size:4rem; font-weight:bold; margin:20px 0;">{st.session_state.score} / {max_possible_score}</div>
        <div style="font-size:1.5rem; margin:10px 0;">Правильных ответов: {st.session_state.correct_count} из {len(st.session_state.questions)}</div>
        <div style="font-size:1.5rem; margin:10px 0;">Результат: {percentage:.0f}%</div>
        <div style="font-size:1.2rem; margin:10px 0; color: #00ff88;">
             Множитель очков: x{POINTS_MULTIPLIER[st.session_state.difficulty]} 
        </div>
    </div>
    """, unsafe_allow_html=True)

    if percentage >= 70:
        st.success(f" Отличный результат! {percentage:.0f}% правильных ответов.")
    elif percentage >= 40:
        st.info(f"Хороший результат! {percentage:.0f}% правильных ответов.")
    else:
        st.warning(f" Результат: {percentage:.0f}%. В следующий раз получится лучше!")


    if not st.session_state.score_saved:
        st.info(f"Игрок: **{st.session_state.player_name}**")

        if st.button("СОХРАНИТЬ РЕЗУЛЬТАТ", use_container_width=True):
            add_score_to_leaderboard(
                st.session_state.player_name,
                st.session_state.score,
                max_possible_score,
                st.session_state.difficulty,
                percentage
            )
            st.session_state.score_saved = True
            st.success(" Результат сохранён в таблицу лидеров!")
            st.rerun()
    else:
        st.info("Ваш результат уже в таблице лидеров!")



def render_leaderboard_widget():
    leaderboard = load_leaderboard()

    with st.expander("ТАБЛИЦА ЛИДЕРОВ", expanded=True):
        if leaderboard:
            for idx, entry in enumerate(leaderboard[:10], 1):
                if idx == 1:
                    medal = "1."
                elif idx == 2:
                    medal = "2."
                elif idx == 3:
                    medal = "3."
                else:
                    medal = f"{idx}."

                if entry["difficulty"] == "easy":
                    diff = "[Л]"
                elif entry["difficulty"] == "medium":
                    diff = "[C]"
                else:
                    diff = "[СЛ]"


                st.markdown(f"""
                <div style='margin: 5px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='width: 40px;'>{medal}</span>
                        <span style='flex: 1; margin-left: 10px;'><b>{entry['name'][:20]}</b></span>
                        <span style='color: #00ff88; font-weight: bold;'>{entry['score']} очков</span>
                        <span style='margin-left: 10px;'>{diff}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Пока нет результатов")

render_leaderboard_widget()

