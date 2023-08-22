# project_cv

Это приложение представляет собой HTTP сервис для работы с импортируемыми данными. Реализована загрузка данных в формате csv (напр. датасеты с Kaggle).

## Интерфейс

- Запрос ``GET``(всего списка): получение списка файлов с информацией о колонках;
- Запрос ``GET``(отдельного файла): получения данных из конкретного файла(по его ``filename``) + возможность фильтрациии и сортировкой по одному или нескольким столбцам;
- Запрос ``POST``: добавление файла;
- Запрос ``DELETE``(всего списка): удаление всего списка файлов;
- Запрос ``DELETE``(отдельного файла): удаление конкретного файла(по его ``filename``);

Хранение данных производится в файле ``my_data.db``, представляющем собой базу данных SQLite3.


## Подготовка и настройка
### Подготовка
Перед запуском системы, необходимо:
- Установить [python3](https://www.python.org/download/releases/3.0/)
- При использовании Visual Studio Code, можно подготовить среду для разработки посредством материалов туториола: https://code.visualstudio.com/docs/python/tutorial-flask

## Запуск приложения
### Запуск сервера
- ``docker build -t adakimov/db_server . && docker run -p 8000:8000 -it adakimov/db_server``

### Настройка клиента
- ``pip install requests``
- ``pip install argparse``


## Работа с сервисом
Для отправки запросов можно использовать утилиту ``curl`` или ``postman``. Но для данного задание написан клиент(client.py). Пример запросов (используем для примера датасет ``Data_Africa.csv``):

Добавление файла:
  
  ```
  python3 client/client.py post -f Data_Africa.csv
  ```
Получение списка файлов с информацией о колонках:
  
  ```
  python3 client/client.py get
  ```
Получения данных из конкретного файла:
  ```
  python3 client/client.py get -f Data_Africa.csv
  ```
Получения данных из файла с каким-то фильтром:
  ```
  python3 client/client.py get -f Data_Africa.csv -fi 'Year < 2003' -fi 'Country == "Republic of the Congo"'
  ```
Получение данных из файла с сортировкой:
  ```
  python3 client/client.py get -f Data_Africa.csv -s 'GDP (USD)'
  ````
Уделение все файлов:
  ```
  python3 client/client.py delete
  ```
Удаление конкретного файла:
  ```
  python3 client/client.py delete -f Data_Africa.csv
  ```
Получение информации о вводе данных:
  ```
  python3 client/client.py -h
  ```
