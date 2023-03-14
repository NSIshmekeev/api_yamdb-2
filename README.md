# api_yamdb
api_yamdb
YaMDb - база данных, которая собирает отзывы о различных произведениях. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». При необходимости, список категорий может быть расширен администратором. Пользователи могут оставлять рецензии на произведения и ставить оценки.

Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc
#### Технологии использованные в проекте:

* Python
* Django
* DRF
* Simple JWT

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VugarIbragimov/api_final_yatube
```

```
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Примеры запросов к API:
 
 ## Регистрация нового пользователя:
```
  [POST].../api/v1/auth/signup/
  {
  "email": "user@example.com",
  "username": "string"
}
```
### Ответ:
```
{
  "email": "user@example.com",
  "username": "string"
}
```
### Получение JWT-токена:
```
    [POST].../api/v1/auth/token/
{
  "username": "string",
  "confirmation_code": "dsfdfsfs844sfsddfd7fs4"
}
```

### Ответ:
```
{
"token": "1161546sdfsdf1sdfdsf6s"
}
```
### Получение списка всех категорий:
```
    [GET].../api/v1/categories/
```
### Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```


### Подробная документация в формате ReDoc доступна по адресу .../redoc/

### Автор проекта:

Иван Афанасьев, Вугар Ибрагимов, Антон Соловьев
