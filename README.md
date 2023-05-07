# Foodgramm - Продуктовый помощник

## Описание проекта

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone git@github.com:YourKeysAreMine/foodgram-project-react.git
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/scripts/activate
```

* Cоздайть файл `.env` в директории `/infra/` с содержанием:

```
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

* Перейти в директорию и установить зависимости из файла requirements.txt:

```bash
cd backend/
pip install -r requirements.txt
```

* Выполнить миграции:

```bash
python manage.py migrate
```

* Запустить сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker compose:
```bash
docker-compose up -d --build
```  
* Подготовьте миграции:
```bash
docker-compose exec web python manage.py makemigrations
```
* Поримените миграции:
```bash
docker-compose exec web python manage.py migrate
```
* Загрузите ингредиенты:
```bash
docker-compose exec web python manage.py import_ingredients_csv
```
* Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## Сайт
Сайт доступен по ссылке:
[]()

## Документация к API
API документация доступна по ссылке (создана с помощью redoc):
[]()

![example workflow](https://github.com/YourKeysAreMine/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Технологии

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Авторы
[Закиров Сергей](https://github.com/YourKeysAreMine)  
