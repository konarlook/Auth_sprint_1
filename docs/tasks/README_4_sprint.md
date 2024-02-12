# Проектная работа 4 спринта

## !!! При проверке

В рамках данного спринта была произведена работа над `etl` и `src`.
Просьба ревьювить данные сервисы (можно конкретнее смотреть по ПР-ам).

## Issues

| Issue |      Участник      |             Статус |
|-------|:------------------:|-------------------:|
| 01    |      samtonck      | :heavy_check_mark: |
| 02    |      samtonck      | :heavy_check_mark: |
| 03    |      samtonck      | :heavy_check_mark: |
| 04    |      samtonck      | :heavy_check_mark: |
| 05    |      RSstrobe      | :heavy_check_mark: |
| 06    |      RSstrobe      | :heavy_check_mark: |
| 08    |      samtonck      | :heavy_check_mark: |
| 09    |      RSstrobe      | :heavy_check_mark: |
| 10    | samtonck, RSstrobe | :heavy_check_mark: |
| 11    |      RSstrobe      | :heavy_check_mark: |
| 12    |      RSstrobe      | :heavy_check_mark: |

Ссылка на репозиторий:
https://github.com/samtonck/4_sprint_team_5

Участники проекта:
Анатолий Кротов https://github.com/samtonck
Григорий Мосягин https://github.com/RSstrobe

## Инструкция по поднятию сервиса

1. Создать в корне проекта `.env` по подобию `.env.example` (для ускорения развертки и проверки переменные окружения
   можно скопировать)
2. Создать в `./app` `.env` по подобию `.env.example` (для ускорения развертки и проверки переменные окружения
   можно скопировать)
3. Создать в `./etl` `.env` по подобию `.env.example` (для ускорения развертки и проверки переменные окружения
   можно скопировать)
4. Создать в `./app` `.env` по подобию `.env.example` (для ускорения развертки и проверки переменные окружения
   можно скопировать)
5. Для запуска проекта необходимо выполнить команду `docker-compose up -d` в корне проекта - `...\4_sprint_team_5`
6. При первичном запуске необходимо запустить скрипт миграции данных из sqlite в Postgres. Это необходимо сделать в
   контейнере `backend`. Команда в
   терминале `docker exec -it backend bash` -> `cd sqlite_to_postgres` -> `python load_data.py`
*. После запуска проекта и миграции бд необходимо подождать 1-2 минуты чтобы данные прокинулись в эластик


Урлы которые пригодятся для проверки:
FastAPI = http://localhost/api/openapi
Elasticvue = http://localhost:8080/
Redisvue = http://localhost:8081/