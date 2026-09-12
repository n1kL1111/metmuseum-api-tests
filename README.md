# Met Museum API Tests

Автоматизированное тестирование **The Metropolitan Museum of Art Collection API** с использованием Python и Pytest.

## О проекте

В проекте реализованы API-тесты для проверки:

* получения информации о произведении искусства;
* обработки запроса несуществующего произведения;
* получения списка произведений;
* поиска произведений по ключевому слову;
* ограничения количества результатов поиска;
* поиска с дополнительными параметрами;
* обработки пустого поискового запроса;
* пагинации результатов поиска.

Ответы API дополнительно валидируются с помощью **Pydantic**.

Для анализа результатов тестирования используется **Allure Report**, а техническая информация о выполнении запросов записывается через стандартный модуль `logging`.

## Технологии

* **Python 3**
* **Pytest** — запуск и организация тестов
* **Requests** — HTTP-запросы к API
* **Pydantic** — валидация структуры ответов
* **Allure** — формирование отчётов
* **Logging** — техническое логирование
* **Git** — контроль версий

## Структура проекта

```text
metmuseum-api-tests/
│
├── api/
│   ├── __init__.py
│   ├── client.py
│   ├── objects.py
│   ├── search.py
│   └── departments.py
│
├── models/
│   ├── __init__.py
│   ├── artwork.py
│   └── object_list.py
│
├── utils/
│   ├── __init__.py
│   └── allure_helpers.py
│
├── tests/
│   ├── test_objects.py
│   └── test_search.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

### Назначение директорий

**`api/`**
Содержит классы для работы с API. HTTP-запросы вынесены отдельно от тестов.

**`models/`**
Содержит Pydantic-модели для валидации ответов API.

**`tests/`**
Содержит непосредственно автоматизированные тесты.

**`utils/`**
Вспомогательные функции проекта.

**`conftest.py`**
Содержит Pytest-фикстуры для создания API-клиентов и HTTP-сессии.

## Проверяемый API

В проекте используется официальный API The Metropolitan Museum of Art:

**The Met Collection API**

Основные используемые endpoints:

```text
GET /public/collection/v1/objects
GET /public/collection/v1/objects/{objectID}
GET /public/collection/v1/departments
GET /public/collection/v1.1/search
```

## Установка

Клонировать репозиторий:

```bash
git clone <URL_REPOSITORY>
cd metmuseum-api-tests
```

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать его (Windows):

```powershell
.venv\Scripts\Activate.ps1
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

## Запуск тестов

Запустить все тесты:

```bash
pytest
```

## Allure Report

Перед использованием скачать Allure:

```bash
npm install -g allure
```

Для формирования отчёта тесты запускаются с указанием директории для результатов Allure:

```bash
pytest --alluredir=allure-results
```

После выполнения тестов будет создана директория:

```text
allure-results/
```

Для просмотра отчёта:

```bash
allure serve allure-results
```

После запуска Allure откроет отчёт в браузере.

## Логирование

Для технического анализа используется стандартный Python `logging`.

В лог записываются:

* HTTP-метод;
* URL запроса;
* query-параметры;
* статус ответа;
* URL фактического запроса;
* информация об ошибках.

Настройки находятся в `pytest.ini`.

Лог выполнения сохраняется в:

```text
logs/test.log
```

Также основные сообщения выводятся непосредственно в консоль во время запуска Pytest.


## Результат

Проект демонстрирует базовые навыки автоматизации REST API:

* работа с HTTP-запросами;
* использование `requests`;
* написание тестов на Pytest;
* работа с параметрами API;
* позитивные и негативные проверки;
* проверка граничных случаев;
* работа с пагинацией;
* валидация JSON через Pydantic;
* логирование;
* формирование Allure-отчётов;
* разделение API-клиента и тестовой логики.

## API Documentation

Официальная документация API:

https://metmuseum.github.io/

```
```

