import pytest
import requests

from api import ApiClient, DepartmentsApi, ObjectsApi, SearchApi
from utils.test_metadata import TEST_METADATA


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


def pytest_collection_modifyitems(items):
    for item in items:
        metadata = TEST_METADATA.get(item.name)

        if metadata:
            item.obj.__allure_display_name__ = metadata["title"]

            item.add_marker(
                pytest.mark.allure_description(
                    metadata["description"]
                )
            )
