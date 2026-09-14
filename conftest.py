import pytest
import requests

from api import ApiClient, DepartmentsApi, ObjectsApi, SearchApi
from utils.test_metadata import TEST_METADATA


PARAMETER_NAMES = {
    "object_id": "ID",
    "keyword": "запрос",
    "query": "запрос",
    "metadata_date": "дата",
    "status_code": "код",
    "department_ids": "отдел",
    "limit": "лимит",
    "offset": "смещение",
    "has_images": "изображения",
    "is_highlight": "выделенное",
    "department_id": "отдел",
    "date_begin": "дата от",
    "date_end": "дата до",
}


@pytest.fixture
def session():
    session = requests.Session()

    yield session

    session.close()


@pytest.fixture
def client(session: requests.Session) -> ApiClient:
    return ApiClient(session)


@pytest.fixture
def objects_api(client: ApiClient) -> ObjectsApi:
    return ObjectsApi(client)


@pytest.fixture
def search_api(client: ApiClient) -> SearchApi:
    return SearchApi(client)


@pytest.fixture
def departments_api(client: ApiClient) -> DepartmentsApi:
    return DepartmentsApi(client)


def pytest_collection_modifyitems(items) -> None:
    for item in items:
        metadata = TEST_METADATA.get(item.originalname)

        if not metadata:
            continue

        title = metadata["title"]

        # Если тест параметризованный,
        # добавляем значения параметров в название
        if hasattr(item, "callspec"):
            params = item.callspec.params

            formatted_params = []

            for name in params:
                display_name = PARAMETER_NAMES.get(name, name)
                formatted_params.append(
                    f"{display_name}: {{{name}}}"
                )

            if formatted_params:
                title += " — " + ", ".join(formatted_params)

        item.obj.__allure_display_name__ = title

        item.add_marker(
            pytest.mark.allure_description(
                metadata["description"]
            )
        )