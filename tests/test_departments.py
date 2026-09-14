from api import DepartmentsApi
from models import DepartmentsList


def test_get_departments(departments_api: DepartmentsApi) -> None:
    response = departments_api.get_departments()

    assert response.status_code == 200, "Неожиданный статус-код"

    data = DepartmentsList.model_validate(response.json())

    assert data.departments, "Список отделов пуст"


def test_departments_have_unique_ids(departments_api: DepartmentsApi) -> None:
    response = departments_api.get_departments()

    assert response.status_code == 200, "Неожиданный статус-код"

    data = DepartmentsList.model_validate(response.json())

    assert data.departments, "Список отделов пуст"

    ids = [d.department_id for d in data.departments]

    assert len(ids) == len(set(ids)), f"ID отделов не уникальны. Дубли: {[i for i in ids if ids.count(i) > 1]}"


def test_departments_have_display_names(departments_api: DepartmentsApi) -> None:
    response = departments_api.get_departments()

    assert response.status_code == 200, "Неожиданный статус-код"

    data = DepartmentsList.model_validate(response.json())

    assert data.departments, "Список отделов пуст"

    for department in data.departments:
        assert department.display_name, f"У отдела {department.department_id} пустой displayName"