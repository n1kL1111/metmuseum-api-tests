import pytest
from api import ObjectsApi
from models import Artwork, ObjectList
from datetime import date

def test_get_artwork(objects_api: ObjectsApi) -> None:
    response = objects_api.get_object(436535)

    assert response.status_code == 200, "Неожиданный статус-код"

    artwork = Artwork.model_validate(response.json())

    assert artwork.object_id == 436535, "Неожиданный ID объекта"
    assert artwork.title == "Wheat Field with Cypresses", "Неожиданное название"
    assert artwork.department == "European Paintings", "Неожиданный отдел"
    assert artwork.object_name == "Painting", "Неожиданное имя объекта"

@pytest.mark.parametrize(
    "object_id",
    [
        0,
        -1,
        99999999999,
    ],
)
def test_get_object_with_invalid_id(objects_api: ObjectsApi, object_id: int) -> None:
    response = objects_api.get_object(object_id)

    assert response.status_code == 404, "Ожидался статус-код 404"

def test_get_objects(objects_api: ObjectsApi) -> None:
    response = objects_api.get_objects(department_ids="11")

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.total > 0, "Общее количество объектов должно быть больше нуля"
    assert result.object_ids, "Список ID объектов пуст"
    assert len(result.object_ids) == len(set(result.object_ids)), "ID объектов должны быть уникальными"

def test_get_objects_by_department(objects_api: ObjectsApi) -> None:
    response = objects_api.get_objects(department_ids="11")

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids, "Список ID объектов пуст"

    for object_id in result.object_ids[:5]:
        object_response = objects_api.get_object(object_id)
        assert object_response.status_code == 200, "Неожиданный статус-код при получении объекта"
        artwork = Artwork.model_validate(object_response.json())
        assert artwork.department == "European Paintings", f"Объект {object_id} принадлежит другому отделу"

@pytest.mark.parametrize(
    "metadata_date, status_code",
    [
        ("2026-08-13", 200),
        ("2025-01-01", 200),
        ("0000-01-01", 200),
        ("2026-13-01", 400),
        ("2026-02-30", 400),
        ("13-08-2026", 400),
        ("invalid-date", 400),
    ],
)
def test_get_date_form(objects_api: ObjectsApi, metadata_date: str, status_code: int) -> None:
    response = objects_api.get_objects(
        metadata_date=metadata_date,
    )

    assert response.status_code == status_code, (f"Для даты '{metadata_date}'"
                                                 f" ожидался код {status_code},"
                                                 f" получен {response.status_code}")

def test_get_objects_by_metadata_date(objects_api: ObjectsApi) -> None:
    metadata_date = "2026-08-13"
    requested = date.fromisoformat(metadata_date)

    response = objects_api.get_objects(metadata_date=metadata_date)
    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())
    assert result.object_ids, "Список ID объектов пуст"

    for object_id in result.object_ids[:5]:
        response = objects_api.get_object(object_id)
        assert response.status_code == 200, "Неожиданный статус-код при получении объекта"
        artwork = Artwork.model_validate(response.json())

        actual = artwork.metadata_date.date()
        assert actual >= requested, (
            f"Дата объекта {object_id} ({actual}) раньше запрошенной ({requested})"
        )
