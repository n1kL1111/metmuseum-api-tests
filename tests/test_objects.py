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
