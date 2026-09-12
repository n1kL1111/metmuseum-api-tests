# 🏛️ Met Museum API Tests

Автоматизированное тестирование **The Metropolitan Museum of Art Collection API** с использованием Python (Pytest, Pydantic).

---

## Что тестируем

В проекте автоматизированы проверки:

* получение информации о произведении искусства;
* обработка запроса с несуществующим ID;
* получение списка произведений;
* поиск произведений по ключевому слову;
* ограничение количества результатов;
* поиск с дополнительными параметрами;
* обработка пустого поискового запроса;
* пагинация результатов поиска.

Ответы API дополнительно валидируются с помощью **Pydantic**.

---

## Покрытие

| Область | Проверка                                     | Тип      |
| ------- | -------------------------------------------- | -------- |
| Objects | Получение произведения по ID                 | Positive |
| Objects | Запрос с несуществующим ID                   | Negative |
| Objects | Получение списка произведений                | Positive |
| Search  | Поиск по ключевому слову                     | Positive |
| Search  | Ограничение количества результатов (`limit`) | Boundary |
| Search  | Фильтр по наличию изображений                | Positive |
| Search  | Пустой поисковый запрос                      | Boundary |
| Search  | Пагинация (`offset`)                         | Boundary |

**Всего: 8 API-тестов**

---

### Основные компоненты

* **`tests/`** — тестовые сценарии и проверки.
* **`api/`** — API-клиенты для работы с отдельными ресурсами.
* **`models/`** — Pydantic-модели для валидации ответов.
* **`utils/`** — вспомогательные функции для Allure.
* **`conftest.py`** — Pytest-фикстуры и настройка тестов.

HTTP-запросы выполняются через общий `ApiClient`, что позволяет не дублировать код в отдельных API-классах.

---

## Технологии

* **Python 3**
* **Pytest** — написание и запуск тестов
* **Requests** — HTTP-запросы
* **Pydantic** — валидация JSON-ответов
* **Allure** — отчётность
* **Logging** — техническое логирование
* **Git** — контроль версий

---

## Структура проекта

```text
metmuseum-api-tests/
│
├── api/
│   ├── client.py
│   ├── departments.py
│   ├── objects.py
│   └── search.py
│
├── models/
│   ├── artwork.py
│   └── object_list.py
│
├── tests/
│   ├── test_objects.py
│   └── test_search.py
│
├── utils/
│   ├── allure_helpers.py
│   └── test_metadata.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

##  Используемый API

В проекте используется официальный **The Metropolitan Museum of Art Collection API**.

Основные endpoints:

```text
GET /public/collection/v1/objects
GET /public/collection/v1/objects/{objectID}
GET /public/collection/v1/departments
GET /public/collection/v1.1/search
```

---

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

---

## Запуск тестов

Запустить все тесты:

```bash
pytest
```

Для запуска с сохранением результатов Allure:

```bash
pytest --alluredir=allure-results
```

Перед этим скачать Allure:

```bash
npm install -g allure
```

---

## 📊 Allure Report

Для анализа результатов тестирования используется **Allure Report**.

Запустить отчёт:

```bash
allure serve allure-results
```

Пример отчёта:

![Allure Overview](docs/allure-overview.png)

---

## 📝 Логирование

Для технического анализа используется стандартный модуль Python `logging`.

В лог записываются:

* HTTP-метод;
* URL запроса;
* query-параметры;
* статус ответа;
* фактический URL;
* ошибки выполнения запроса.

Лог сохраняется в:

```text
logs/test.log
```

Основная информация также выводится в консоль при запуске Pytest.

## 📚 Документация API

Официальная документация:

https://metmuseum.github.io/
