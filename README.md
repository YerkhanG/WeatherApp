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
## Описание API
API_KEY:
В файле settings.py укажите ваш StormGlass API ключ:
```python
API_KEY = "ваш_ключ_от_StormGlass"
```
1. Регистрация пользователя
URL: /register_user/
Метод: POST
Параметры (формат application/x-www-form-urlencoded):
username – имя пользователя (строка, обязательный)
password – пароль (строка, обязательный)
city – город (строка, обязательный)
Пример запроса (curl):
```bash
curl -X POST -d "username=johndoe&password=secret123&city=Almaty" http://localhost:8000/register_user/ 
```
2. Получение токена
Чтобы получить токен для пользователя, воспользуйтесь стандартным DRF эндпоинтом.
```bash
curl -X POST -d "username=johndoe&password=secret123" http://localhost:8000/api-token-auth/
```
3. Получение погоды пользователя
URL: /user_weather/
Метод: GET
Аутентификация: Токен-аутентификация (DRF)
Описание:
Возвращает данные о погоде для города, указанного в профиле авторизованного пользователя. Если данные в кэше актуальны (меньше 10 минут), они возвращаются из базы, иначе происходит запрос к StormGlass API.
Пример запроса (curl):
```bash
curl -H "Authorization: Token <ваш токен>" http://localhost:8000/user_weather/
```
4. Добавление города (Менеджеры)
URL: /add-city/
Метод: POST
Аутентификация: Токен-аутентификация (DRF)
Требование: Пользователь должен состоять в группе "Managers"
Параметры (JSON):
city – название города (обязательно)
Пример запроса (curl):
```bash
curl -X POST -H "Authorization: Token <ваш токен>"" -H "Content-Type: application/json" -d "{\"city\": \"NewYork\"}" http://localhost:8000/add-city/
```
