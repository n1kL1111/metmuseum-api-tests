import allure

from models import ObjectList
from utils.allure_helpers import attach_response


@allure.title("Поиск произведений по ключевому слову")
@allure.description("Проверка поиска произведений по ключевому слову")
def test_search_by_keyword(search_api):
    with allure.step("Выполнить поиск по слову cats"):
        response = search_api.search("cats")

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код"):
        assert response.status_code == 200

    with allure.step("Валидировать ответ через Pydantic"):
        result = ObjectList.model_validate(response.json())

    with allure.step("Проверить результаты поиска"):
        assert result.total > 0
        assert result.objectIDs


@allure.title("Ограничение количества результатов поиска")
@allure.description("Проверка параметра limit")
def test_search_limit(search_api):
    limit = 10

    with allure.step(f"Выполнить поиск с limit={limit}"):
        response = search_api.search(
            "cats",
            limit=limit,
        )

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код"):
        assert response.status_code == 200

    with allure.step("Валидировать ответ через Pydantic"):
        result = ObjectList.model_validate(response.json())

    with allure.step("Проверить количество результатов"):
        assert len(result.objectIDs) <= limit


@allure.title("Поиск с фильтром наличия изображений")
@allure.description("Проверка выполнения поиска с параметром hasImages")
def test_search_with_filter(search_api):
    with allure.step("Выполнить поиск с фильтром hasImages"):
        response = search_api.search(
            "cats",
            has_images=True,
            limit=5,
        )

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код"):
        assert response.status_code == 200

    with allure.step("Валидировать ответ через Pydantic"):
        result = ObjectList.model_validate(response.json())

    with allure.step("Проверить результаты поиска"):
        assert result.objectIDs
        assert len(result.objectIDs) <= 5


@allure.title("Поиск с пустым запросом")
@allure.description("Проверка обработки пустого поискового запроса")
def test_search_empty_query(search_api):
    with allure.step("Выполнить поиск с пустым запросом"):
        response = search_api.search("")

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код"):
        assert response.status_code == 200

    with allure.step("Валидировать ответ через Pydantic"):
        result = ObjectList.model_validate(response.json())

    with allure.step("Проверить структуру ответа"):
        assert isinstance(result.total, int)
        assert isinstance(result.objectIDs, list)


@allure.title("Пагинация результатов поиска")
@allure.description("Проверка параметра offset")
def test_search_offset(search_api):
    with allure.step("Получить первую страницу результатов"):
        first_response = search_api.search(
            "cats",
            offset=0,
            limit=5,
        )

    with allure.step("Получить вторую страницу результатов"):
        second_response = search_api.search(
            "cats",
            offset=5,
            limit=5,
        )

    with allure.step("Добавить первый ответ в отчёт"):
        attach_response(first_response)

    with allure.step("Добавить второй ответ в отчёт"):
        attach_response(second_response)

    with allure.step("Проверить статус-коды"):
        assert first_response.status_code == 200
        assert second_response.status_code == 200

    with allure.step("Валидировать ответы через Pydantic"):
        first = ObjectList.model_validate(first_response.json())
        second = ObjectList.model_validate(second_response.json())

    with allure.step("Проверить результаты пагинации"):
        assert first.objectIDs
        assert second.objectIDs
        assert first.objectIDs != second.objectIDs

