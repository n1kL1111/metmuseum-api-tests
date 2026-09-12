import pytest
import requests

from api import ApiClient, DepartmentsApi, ObjectsApi, SearchApi
from utils.test_metadata import TEST_METADATA, FILE_NAMES


@pytest.fixture
def session():
    session = requests.Session()

    yield session

    session.close()


@pytest.fixture
def client(session):
    return ApiClient(session)


@pytest.fixture
def objects_api(client):
    return ObjectsApi(client)


@pytest.fixture
def search_api(client):
    return SearchApi(client)


@pytest.fixture
def departments_api(client):
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

        suite_name = FILE_NAMES.get(item.path.name)

        if suite_name:
            item.add_marker(
                pytest.mark.allure_label(
                    suite_name,
                    label_type="suite",
                )
            )
