# YATUBE

### Краткое описание проекта

Django-проект небольшой соц. сети. В проекте реализованы механизмы аутентификации, создания и удаления постов, комментариев, подписки на авторов. Проект может быть использован для публичного или приватного ведения личных дневников с возможностью обсуждения в диалоговом пространстве

### Установка проекта на локальном компьютере

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Skakovsku/hw05_final
```
Перейти в корневую папку склонированного проекта:
```
cd hw05_final
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```
При активированном виртуальном окружении создайте суперпользователя:
```
python3 manage.py createsuperuser
```

Запустить проект на локальном рабочем сервере:

```
python3 manage.py runserver
```
