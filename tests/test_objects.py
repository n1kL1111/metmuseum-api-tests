from api import ObjectsApi
from models import Artwork, ObjectList
import pytest

def test_get_artwork(objects_api: ObjectsApi) -> None:
    response = objects_api.get_object(436535)

    assert response.status_code == 200, "Unexpected status code"

    artwork = Artwork.model_validate(response.json())

    assert artwork.object_id == 436535, "Unexpected object ID"
    assert artwork.title == "Wheat Field with Cypresses", "Unexpected title"
    assert artwork.department == "European Paintings", "Unexpected department"
    assert artwork.object_name == "Painting", "Unexpected name"

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

    assert response.status_code == 404, "Unexpected status code"

def test_get_objects(objects_api: ObjectsApi) -> None:
    response = objects_api.get_objects()
    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.total > 0, "Unexpected total"
    assert result.object_ids, "Object IDs list is empty"
    assert len(result.object_ids) == result.total, "Number of object IDs does not match total"

def test_object_ids_are_unique(objects_api: ObjectsApi) -> None:
    response = objects_api.get_objects()

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert len(result.object_ids) == len(set(result.object_ids)), "Object IDs must be unique"

def test_get_objects_by_department(objects_api: ObjectsApi) -> None:
    response = objects_api.get_objects(department_ids="11")

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())
    for object_id in result.object_ids[:10]:
        object_response = objects_api.get_object(object_id)
        assert object_response.status_code == 200, "Unexpected status code"
        artwork = Artwork.model_validate(object_response.json())
        assert artwork.department == "European Paintings", "Unexpected department"
    assert result.object_ids, "Expected object IDs"

def test_object_ids_can_be_retrieved(objects_api: ObjectsApi) -> None:
    response = objects_api.get_objects()

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    for object_id in result.object_ids[:5]:
        object_response = objects_api.get_object(object_id)

        assert object_response.status_code == 200, "Unexpected status code"

        artwork = Artwork.model_validate(object_response.json())

        assert artwork.object_id == object_id, "Unexpected object ID"

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

    assert response.status_code == status_code, "Unexpected status code"



def test_get_objects_by_metadata_date(objects_api: ObjectsApi) -> None:
    metadata_date = "2026-08-13"

    response = objects_api.get_objects(metadata_date=metadata_date)

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids, "Object IDs list is empty"

    for object_id in result.object_ids[:10]:
        response = objects_api.get_object(object_id)

        assert response.status_code == 200, f"Unexpected status code"

        artwork = Artwork.model_validate(response.json())

        actual_date = artwork.metadata_date[:10]

        assert actual_date >= metadata_date, "Unexpected date"
