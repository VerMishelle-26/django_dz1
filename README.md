# Django DRF Project — Employees & Workplaces API

REST API для управления сотрудниками и рабочими местами на Django + DRF.
Реализованы CRUD, JWT-авторизация, ролевая модель прав, фильтрация, пагинация,
документация Swagger и контейнеризация через Docker Compose.

## Стек

- Python 3.12, Django 6.1, Django REST Framework
- SimpleJWT, django-filter, drf-spectacular, django-cors-headers
- PostgreSQL (в Docker) / SQLite (локально)
- Docker + Docker Compose

## Эндпоинты

| Метод | URL | Описание | Доступ |
|---|---|---|---|
| GET | /api/employees/ | Список сотрудников (пагинация по 10) | Все |
| GET | /api/employees/?page=N | Постраничный вывод | Все |
| GET | /api/employees/?skills=python&min_experience_days=365&role=dev | Фильтр по навыкам, стажу, роли | Все |
| GET | /api/employees/{id}/ | Подробная информация о сотруднике | Все |
| POST | /api/employees/ | Добавление сотрудника | Администратор |
| PUT/PATCH | /api/employees/{id}/ | Изменение | Администратор |
| DELETE | /api/employees/{id}/ | Удаление | Администратор |
| GET | /api/workplaces/ | Список рабочих мест | Все |
| PATCH | /api/workplaces/{id}/ | Перемещение сотрудника между столами | Смотритель, Администратор |
| POST | /api/token/ | Получение JWT | Все |
| POST | /api/token/refresh/ | Обновление access-токена | Все |
| GET | /api/docs/ | Swagger-документация | Все |

## Роли

- **Посетитель** — только просмотр (GET).
- **Смотритель** — просмотр + перемещение сотрудников между столами (PATCH).
- **Администратор** — полный CRUD + перемещение.

## Запуск через Docker Compose

1. Клонировать репозиторий:

   git clone https://github.com/VerMishelle-26/django_dz1.git
   cd django_dz1

2. Создать файл `.env` в корне:

   DJANGO_SECRET_KEY=change_me
   DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   POSTGRES_DB=django_db
   POSTGRES_USER=django_user
   POSTGRES_PASSWORD=django_password

3. Собрать и запустить:

   docker-compose up -d --build

4. Применить миграции (если не применились автоматически):

   docker-compose exec web python manage.py migrate

5. Создать суперпользователя:

   docker-compose exec web python manage.py createsuperuser

6. Создать группы прав:

   docker-compose exec web python manage.py shell

   В открывшейся консоли:

   from django.contrib.auth.models import Group
   [Group.objects.get_or_create(name=n) for n in ["Посетитель", "Смотритель", "Администратор"]]
   exit()

7. Открыть в браузере:

   - API: http://localhost:8000/api/
   - Swagger: http://localhost:8000/api/docs/
   - Админка: http://localhost:8000/admin/

Остановить:

   docker-compose down

## Локальный запуск (без Docker)

1. Клонировать репозиторий и перейти в папку:

   git clone https://github.com/VerMishelle-26/django_dz1.git
   cd django_dz1

2. Создать и активировать venv:

   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Установить зависимости:

   pip install -r requirements.txt

4. Применить миграции:

   python manage.py migrate

5. Создать суперпользователя:

   python manage.py createsuperuser

6. Создать группы прав:

   python manage.py shell

   from django.contrib.auth.models import Group
   [Group.objects.get_or_create(name=n) for n in ["Посетитель", "Смотритель", "Администратор"]]
   exit()

7. Запустить сервер:

   python manage.py runserver

8. Открыть:

   - API: http://127.0.0.1:8000/api/
   - Swagger: http://127.0.0.1:8000/api/docs/
   - Админка: http://127.0.0.1:8000/admin/

## JWT-авторизация

Получить токен:

   POST /api/token/
   Content-Type: application/json

   {"username": "user", "password": "pass"}

Ответ:

   {"refresh": "eyJ...", "access": "eyJ..."}

Использование:

   GET /api/employees/
   Authorization: Bearer <access_token>

## CORS

Настраивается в config/settings.py:

   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:8000",
   ]

Для разработки можно временно включить CORS_ALLOW_ALL_ORIGINS = True.

## Стиль кода

- Black (форматирование)
- isort (сортировка импортов)

Применить:

   black .
   isort .

## Структура

   django_dz1/
   ├── config/          # настройки
   ├── employees/       # сотрудники
   ├── workplaces/      # рабочие места
   ├── templates/
   ├── static/
   ├── media/
   ├── Dockerfile
   ├── docker-compose.yml
   ├── .env.example
   ├── requirements.txt
   ├── manage.py
   └── README.md

## Автор

Вероника Мишель — https://github.com/VerMishelle-26