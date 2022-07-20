## Разворачивание окружения

Первая задача – развернуть проект в продакшен среде. Проект должен быть развернут на Heroku. Для нашего проекта будет достаточно бесплатных планов, которые включают в себя работу с базой данных PostgreSQL.

### Требования к проекту

* Проект должен быть реализован на [poetry](https://python-poetry.org/)
* При инициализации пакета задайте имя `hexlet-code`
* Проект должен содержать приложение Flask с именем `page_analyzer`, содержащее модуль `app`. Другими словами, проект, который мы разрабатываем, можно использовать снаружи:

    ```python
    from page_analyzer import app
    ```

### Ссылки

* [Документация Django](https://docs.djangoproject.com/en/4.0/)
* [Getting Started on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
* [Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [dj-database-url](https://pypi.org/project/dj-database-url/)
* [The Twelve-Factor App](https://12factor.net/ru/)
* [Зачем нужны логи в веб-приложениях и как они выглядят](https://guides.hexlet.io/ru/logging/)

### Задачи

* Убедитесь, что вы используете Python версии 3.8 или выше
* Настройте базовое окружение, которое после старта на http-запрос на главную страницу (`/`) выдаёт приветствие
* Подключите линтер и настройте Github Actions
* Заведите аккаунт на Heroku. Если вы из РФ, вам необходимо [подключить VPN](https://github.com/Hexlet/hexlet-unblock) и указать другую страну. Выполните деплой
* Задеплойте то, что получилось, на Heroku. Этот пункт крайне важно выполнить, как можно раньше. Нет ничего важнее, чем быстрая доставка (читаем ["Цель"](https://ru.hexlet.io/pages/recommended-books) и знакомимся с DevOps)
* Добавьте в README.md ссылку на Heroku-домен, по которой можно посмотреть то, что получилось

### Подсказки

* Управление настройками через пакет `python-dotenv`
* Секреты (любые доступы) должны передаваться через переменные окружения, по понятным причинам их нельзя хранить в репозитории