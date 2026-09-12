from models import Artwork


def test_get_artwork(objects_api):
    response = objects_api.get_object(436535)

    assert response.status_code == 200

    artwork = Artwork.model_validate(response.json())

    assert artwork.objectID == 436535
    assert artwork.title
    assert artwork.department


def test_get_nonexistent_artwork(objects_api):
    response = objects_api.get_object(999999999)

    assert response.status_code == 404


def test_get_objects(objects_api):
    response = objects_api.get_objects()

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "objectIDs" in data
    assert isinstance(data["total"], int)
    assert isinstance(data["objectIDs"], list)
