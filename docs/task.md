## 📦 Inventory Reservation Service

Микросервис для временного резервирования товаров на маркетплейсе. Решает задачу "overselling" (продажи большего количества товара, чем есть на складе) и автоматического освобождения остатков.

## 🛠 Технологический стек
- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL (SQLAlchemy + Alembic)
- **Concurrency & Locking:** Redis
- **Background Tasks:** APScheduler (авто-снятие резервов по TTL)
- **Containerization:** Docker & Docker Compose
- **Testing:** Pytest

## Термины
- SKU — конкретная позиция товара
- Stock — текущий остаток на складе
Reservation — временная блокировка части остатка**
## Цель
Разработать сервис резервирования остатков:
- создаёт резерв на SKU,
- подтверждает резерв при оформлении заказа,
- снимает резерв автоматически по TTL,
- выдерживает конкурентные запросы.

## Задачи
 - Создание приложения app, которое получает post запросы, работает с базой данной и отдает ответ клиенту
 - Создание БД на Postgres, миграция моделей с помощью SQLAlchemy + Alembic
 - Прописать минимальные тесты
 - Развернуть архитектуру с помощью Docker

## Структура

```
FastAPIozonMarketplace/                 # Корневая директория проекта
├── app/                               # Основное приложение
│   ├── models/
│   │   ├── database.py               # Конфигурация и подключение к БД
│   │   └── models.py                 # SQLAlchemy/Pydantic модели данных
│   ├── serializers/
│   │   └── stocks_serializers.py     # Схемы для операций с остатками товаров
│   ├── service/
│   │   ├── service.py                # Основные сервисные функции
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py                       # Точка входа FastAPI приложения, маршруты
├── db/                                # Работа с миграциями БД
│   ├── alembic/                       # Конфигурация Alembic для миграций
│   │   ├── versions/                  # Папка с файлами миграций
│   │   ├── __init__.py
│   │   ├── env.py                    # Конфигурация окружения Alembic
│   │   ├── README
│   │   └── script.py.mako
│   └── __init__.py
├── tests/                             # Тесты приложения
│   ├── __init__.py
│   ├── conftest.py                    # Фикстуры pytest для тестов
│   └── test_main.py                   # Тесты основного приложения
├── alembic.ini                        # Конфигурационный файл Alembic
├── docker-compose.yml                 # Конфигурация Docker Compose для запуска сервисов
├── Dockerfile                         # Инструкции для сборки Docker-образа
├── README.md                          # Документация проекта
└── requirements.txt                   # Зависимости Python-проекта
```
## Как упаковать сам проект и запустить

### 1. Скачайте Docker Desctop
Без него будет почти невозможно запустить и отслеживать ресурсы
[Docker Desktop: The #1 Containerization Tool for Developers | Docker](https://www.docker.com/products/docker-desktop/)

### 2. Запуск Docker
После установки, заходим в корневую папку с проектом и запускаем сборку Docker(все уже настроено)
```bush
docker-compose up -d --build
```
Это поднимет три сервиса:
- `app` (FastAPI на порту 8000)
- `db` (PostgreSQL на порту 5432)
- `redis` (Redis на порту 6379)

Для того чтобы отслеживать весь процесс, рекомендуется использовать команду указанную ниже, там должно запущенно быть 3 процесса. Если их меньше, то проект не правильно собрался, рекомендуется пересборка
```bush
docker ps
```

После удачной сборки, воспользуйтесь миграцией, чтобы заполнить БД.
```bush
alembic upgrade head
```

После всех пройденных пунктов, с помощью Postman([Download Postman | Get Started for Free](https://www.postman.com/downloads/)) вы можете протестировать все post запросы.
### 3. Запуск авто тестов
Если вы хотите протестировать продукт с помощью авто тестов, то в папке проекта, вам надо войти в папку тестов и воспользоваться pytest, перед этим установив предварительно библиотеку.
```cmd
cd tests
python -m pytest
```

## 🧩 Ключевые особенности реализации

### Конкурентность (Race Condition Protection)

Для предотвращения двойного списания товара используется **распределенная блокировка в Redis** по ключу SKU.

1. При запросе на резерв сервис захватывает Lock в Redis.
2. Выполняется проверка остатка в БД (используется `SELECT ... FOR UPDATE` в транзакции).
3. Создается резерв и обновляется `reserved_qty`.
4. Lock освобождается.

### Автоматическое снятие резервов (TTL)

В приложении запущен фоновый планировщик `APScheduler`, который каждые 30 секунд сканирует таблицу `reservations`. Если текущее время больше `expires_at` и статус резерва `active`, он переводится в `expired`, а заблокированное количество товара возвращается в доступный остаток склада.

```python
@asynccontextmanager  
async def lifespan(app: FastAPI):  
    scheduler = BackgroundScheduler()  
  
    scheduler.add_job(expire_reservations_task, 'interval', seconds=30)  
    scheduler.start()  
    yield  
    scheduler.shutdown()  
  
app = FastAPI(lifespan=lifespan)
```

## 📊 Модель данных

- **Stocks**: `sku`, `total_qty`, `reserved_qty`, `updated_at`.
```python
class StocksBase(Base):  
    __tablename__ = 'stocks'  
  
    id: Mapped[int] = mapped_column(primary_key=True)  
    sku: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)  
    total_qty: Mapped[int] = mapped_column(default=0, nullable=False)  
    reserved_qty: Mapped[int] = mapped_column(default=0, nullable=False)  
    updated_at: Mapped[datetime] = mapped_column(  
        default=func.now(),  
        onupdate=func.now(),  
        nullable=False  
    )
```

- **Reservations**: `id`, `sku_id`, `qty`, `status` (active, confirmed, canceled, expired), `expires_at`, `order_id`.
```python
class ReservationsBase(Base):  
    __tablename__ = 'reservations'  
  
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)  
    sku: Mapped[int] = mapped_column(ForeignKey('stocks.id'))  
    qty: Mapped[int] = mapped_column(default=1)  
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus), default=ReservationStatus.ACTIVE)  
    created_at: Mapped[datetime] = mapped_column(  
        default=func.now(),  
        nullable=False  
    )  
    expires_at: Mapped[datetime] = mapped_column(nullable=False)  
    order_id: Mapped[str] = mapped_column(  
    String(30),  
        unique=True,  
        nullable=True  
    )
```
