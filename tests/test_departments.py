from api import DepartmentsApi
from models import DepartmentsList


def test_get_departments(departments_api: DepartmentsApi) -> None:
    response = departments_api.get_departments()

    assert response.status_code == 200, "Неожиданный статус-код"

    data = DepartmentsList.model_validate(response.json())

    assert data.departments, "Список отделов пуст"

    ids = [department.department_id for department in data.departments]

    assert len(ids) == len(set(ids)), "ID отделов должны быть уникальными"

    for department in data.departments:
        assert department.display_name, f"У отдела {department.department_id} отсутствует displayName"
