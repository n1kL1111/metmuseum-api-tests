import allure

from models import Artwork
from utils.allure_helpers import attach_response


@allure.title("Получение произведения искусства по ID")
@allure.description("Проверка получения существующего произведения искусства")
def test_get_artwork(objects_api):
    with allure.step("Отправить GET-запрос"):
        response = objects_api.get_object(436535)

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код"):
        assert response.status_code == 200

    with allure.step("Валидировать ответ через Pydantic"):
        artwork = Artwork.model_validate(response.json())

    with allure.step("Проверить данные произведения"):
        assert artwork.objectID == 436535
        assert artwork.title
        assert artwork.department


@allure.title("Получение несуществующего произведения")
@allure.description("Проверка обработки запроса с несуществующим ID")
def test_get_nonexistent_artwork(objects_api):
    with allure.step("Отправить GET-запрос с несуществующим ID"):
        response = objects_api.get_object(999999999)

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код 404"):
        assert response.status_code == 404


@allure.title("Получение списка произведений")
@allure.description("Проверка получения списка идентификаторов произведений")
def test_get_objects(objects_api):
    with allure.step("Отправить GET-запрос"):
        response = objects_api.get_objects()

    with allure.step("Добавить данные запроса и ответа в отчёт"):
        attach_response(response)

    with allure.step("Проверить статус-код"):
        assert response.status_code == 200

    with allure.step("Проверить структуру ответа"):
        data = response.json()

        assert "total" in data
        assert "objectIDs" in data
        assert isinstance(data["total"], int)
        assert isinstance(data["objectIDs"], list)

    assert response.status_code == 404

def test_get_objects(objects_api):
    response = objects_api.get_objects()

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "objectIDs" in data
    assert isinstance(data["total"], int)
    assert isinstance(data["objectIDs"], list)
