## Ссылки

1) [Ссылка на Docker образ ETL](https://hub.docker.com/r/vadimiki/etl)
2) [Ссылка на GitHub репозиторий ETL](https://github.com/abandonedv/new_admin_panel_sprint_3)

## Инструкция по запуску:

1) Клонируем репозиторий:
   ```
   git clone https://github.com/abandonedv/Async_API_sprint_2.git
   ```
2) Заходим в корневую директрию проекта `/Async_API_sprint_2`:
   ```
   cd path/to/Async_API_sprint_2
   ```
3) Создаем файл `.env` и копируем в него содержимое файла `.env.example`:
   ```
   cp .env.example .env
   ```
4) Запускаем сервисы:
   ```
   docker-compose up
   ```

5) [Ссылка на документацию запущенного приложения](http://127.0.0.1/api/openapi)

6) Все должно работать!

## Тесты:

1) Запускаем тестовые сервисы:
   ```
   docker-compose -f app/tests/functional/docker-compose.yml up
   ```
   
2) Смотрим логи тестов:
   ```
   docker-compose -f app/tests/functional/docker-compose.yml logs -f tests
   ```

3) Тесты должны выполниться успешно!
