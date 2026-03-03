"""
Главное приложение. Отображает меню и запускает выбранные демонстрации.
"""

import sys
from logic import (
    demo_create_simple_table,
    demo_read_data,
    demo_append_data,
    demo_formulas,
    demo_formatting,
    demo_chart,
    demo_multiple_sheets
)
from utils import print_header


def show_menu():
    """Выводит главное меню."""
    menu_text = """
============================================================
           📦 ДЕМОНСТРАЦИОННЫЙ СТЕНД OPENPYXL            
============================================================
1. 📄 Создание простой таблицы (запись данных)
2. 📖 Чтение данных из Excel
3. ➕ Добавление новых данных
4. 🧮 Работа с формулами
5. 🎨 Форматирование ячеек (цвет, шрифт)
6. 📊 Создание диаграммы
7. 📑 Работа с несколькими листами
0. ❌ Выход
------------------------------------------------------------
👉 Выберите демонстрацию (0-7): """
    return input(menu_text)


def main():
    """Главный цикл программы."""
    while True:
        choice = show_menu().strip()

        if choice == "1":
            demo_create_simple_table()
        elif choice == "2":
            demo_read_data()
        elif choice == "3":
            demo_append_data()
        elif choice == "4":
            demo_formulas()
        elif choice == "5":
            demo_formatting()
        elif choice == "6":
            demo_chart()
        elif choice == "7":
            demo_multiple_sheets()
        elif choice == "0":
            print_header("До свидания!")
            sys.exit(0)
        else:
            print("❌ Неверный ввод. Пожалуйста, введите цифру от 0 до 7.")

        input("\nНажмите Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    main()
