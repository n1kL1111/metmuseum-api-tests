from models import Artwork, ObjectList


def test_get_artwork(objects_api) -> None:
    response = objects_api.get_object(436535)

    assert response.status_code == 200, "Unexpected status code"

    artwork = Artwork.model_validate(response.json())

    assert artwork.object_id == 436535, "Unexpected object ID"
    assert artwork.title == "Wheat Field with Cypresses", "Unexpected title"
    assert artwork.department == "European Paintings", "Unexpected department"


def test_get_nonexistent_artwork(objects_api) -> None:
    response = objects_api.get_object(999999999)

    assert response.status_code == 404, "Expected 404 for invalid ID"


def test_get_objects(objects_api) -> None:
    response = objects_api.get_objects()
    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())
    assert result.total == 502726, "Unexpected total"
    assert result.object_ids, "Object IDs list is empty"
