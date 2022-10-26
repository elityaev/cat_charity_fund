<h2 align="center">QRkot</h2>


### Описание

---
QRkot - это API сервис для сбора пожертвований в благотворительные 
проекты. В проекте реализованы функции создания благотворительны 
проектов, внесения пожертвований, автоматическое их распределение 
по открытым проектам в порядке очереди (First In, First Out). 
Настроена системы аутентификации и авторизации пользователей. 
При запуске проекта автоматически создается суперюзер.

### Технологии и библиотеки

---
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
* [Pydantic](https://pypi.org/project/pydantic/)
* [Alembic](https://pypi.org/project/alembic/)
* [Asyncio](https://docs.python.org/3/library/asyncio.html)

### Установка и запуск

---
1. Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:elityaev/cat_charity_fund.git
```

2. Создать и активировать виртуальное окружение,
обновить библиотеку pip, установить зависимости:

```
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3. В корневой директории создать и заполнить env-файл 
по следующему шаблону:

```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
DATABASE_URL=sqlite+aiosqlite:///./<название базы данных>.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>
```
4. Применить миграции для создания БД

```
alembic upgrade head
```

5. Запустить локальный сервер  

```
uvicorn app.main:app --reload

```

 Документация к API будет доступна по следующим адресам:



*[http://127.0.0.1:8000/docs ](http://127.0.0.1:8000/docs)* - Swagger

*[http://127.0.0.1:8000/docs ](http://127.0.0.1:8000/docs)* - ReDoc
___

#### Автор

_Литяев Евгений_



