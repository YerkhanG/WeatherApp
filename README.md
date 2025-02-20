# Weather App
Это Django-приложение предоставляет информацию о погоде для указанного города. Проект реализует следующие возможности:

Регистрация пользователя с автоматическим созданием профиля, где пользователь выбирает город.
Просмотр погодных данных для города, указанного в профиле.
Менеджеры (пользователи, входящие в группу "Managers") могут добавлять новые города.
## Установка и запуск проекта
Клонирование репозитория:
```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```
Создание и активация виртуального окружения:
```bash
python -m venv .venv
source .venv/bin/activate   # для Linux/MacOS
.venv\Scripts\activate      # для Windows
```
Установка зависимостей:
```bash
pip install -r requirements.txt
```
Проект использует PostgreSQL. Убедитесь, что база данных создана. B PostgreSQL создайте базу данных:
```sql
CREATE DATABASE weather_app;
```
Применение миграций и запуск сервера:
```bash
python manage.py migrate
python manage.py runserver
```
