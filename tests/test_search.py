from models import ObjectList


def test_search_by_keyword(search_api):
    response = search_api.search("cats")

    assert response.status_code == 200

    result = ObjectList.model_validate(response.json())

    assert result.total > 0
    assert result.objectIDs


def test_search_limit(search_api):
    limit = 10

    response = search_api.search(
        "cats",
        limit=limit,
    )

    assert response.status_code == 200

    result = ObjectList.model_validate(response.json())

    assert len(result.objectIDs) <= limit


def test_search_with_filter(search_api):
    response = search_api.search(
        "cats",
        has_images=True,
        limit=5,
    )

    assert response.status_code == 200

    result = ObjectList.model_validate(response.json())

    assert result.objectIDs
    assert len(result.objectIDs) <= 5