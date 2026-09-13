from api import SearchApi, ObjectsApi
from models import ObjectList, Artwork
import pytest

def test_search_by_keyword(search_api: SearchApi, objects_api: ObjectsApi ) -> None:
    keyword = "Rembrandt"

    response = search_api.search(keyword, limit=10)

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids, "Search returned no results"

    for object_id in result.object_ids:
        object_response = objects_api.get_object(object_id)

        assert object_response.status_code == 200, "Unexpected status code"

        artwork = Artwork.model_validate(object_response.json())

        assert keyword.lower() in artwork.artist_display_name.lower(), f"Keyword not found for object {object_id}"

def test_search_by_invalid_keyword(search_api: SearchApi) -> None:
    response = search_api.search("qwerty")

    assert response.status_code == 200, "Unexpected status code"

    assert response.json()["total"] == 0, "Expected zero results"

def test_search_limit(search_api: SearchApi) -> None:
    response = search_api.search("Rembrandt", limit=10)

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.total >= 10, "Expected at least 10 results"
    assert len(result.object_ids) == 10, "Unexpected number of results"

def test_search_with_filter(search_api: SearchApi) -> None:
    response = search_api.search("Rembrandt", has_images=True, limit=10)

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids, "Object IDs list is empty"
    assert len(result.object_ids) <= 10, "Unexpected object count"

def test_search_limit_exceeded(search_api: SearchApi) -> None:
    response = search_api.search(
        "cats",
        limit=501,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert len(result.object_ids) <= 500, "Limit exceeded"

def test_search_max_limit(search_api: SearchApi) -> None:
    response = search_api.search(
        "cats",
        limit=500,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert len(result.object_ids) == 500, "Unexpected object count"

def test_search_empty_query(search_api: SearchApi) -> None:
    response = search_api.search("")

    assert response.status_code == 200, "Unexpected status code"

    ObjectList.model_validate(response.json())

@pytest.mark.parametrize(
    "offset, expected_object_ids",
    [
        (
            0,
            [437403, 437420, 437406, 437416, 437418, 437414, 437411, 437419, 437404, 437407],
        ),
        (
            10,
            [359970, 437408, 437409, 437410, 437413, 437421, 438379, 354638, 391544, 459194],
        ),
        (
            20,
            [437412, 354635, 337491, 364151, 364152, 364153, 373068, 437390, 370641, 437397],
        ),
    ],
)
def test_search_offset(search_api: SearchApi, offset: int, expected_object_ids: list[int]) -> None:
    response = search_api.search(
        "Rembrandt",
        offset=offset,
        limit=10,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids == expected_object_ids, "Unexpected object IDs"
