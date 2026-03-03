"""
Модуль содержит классы данных и функции для генерации примеров.
"""

import random
from datetime import datetime, timedelta


class Employee:
    """Модель сотрудника."""
    def __init__(self, emp_id, name, department, salary, hire_date):
        self.id = emp_id
        self.name = name
        self.department = department
        self.salary = salary
        self.hire_date = hire_date


class Sale:
    """Модель продажи."""
    def __init__(self, sale_id, product, quantity, price, date):
        self.id = sale_id
        self.product = product
        self.quantity = quantity
        self.price = price
        self.date = date


def generate_sample_employees(count=5):
    """Генерирует список сотрудников для демонстрации."""
    departments = ['IT', 'Sales', 'HR', 'Finance', 'Marketing']
    first_names = ['Иван', 'Петр', 'Сергей', 'Анна', 'Елена', 'Ольга']
    last_names = ['Иванов', 'Петров', 'Сидоров', 'Кузнецова', 'Смирнова']

    employees = []
    for i in range(1, count + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        dept = random.choice(departments)
        salary = random.randint(50000, 150000)
        hire_date = datetime.now() - timedelta(days=random.randint(30, 1000))
        employees.append(Employee(i, name, dept, salary, hire_date.date()))
    return employees


def generate_sample_sales(count=8):
    """Генерирует список продаж."""
    products = ['Ноутбук', 'Мышь', 'Клавиатура', 'Монитор', 'Принтер']
    sales = []
    for i in range(1, count + 1):
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = random.randint(1000, 50000)
        date = datetime.now() - timedelta(days=random.randint(0, 30))
        sales.append(Sale(i, product, quantity, price, date.date()))
    return sales
