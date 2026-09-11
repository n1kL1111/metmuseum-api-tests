import pytest
import requests

from api import ApiClient, DepartmentsApi, ObjectsApi, SearchApi


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

