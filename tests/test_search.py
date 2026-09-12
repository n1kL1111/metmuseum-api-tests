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


def test_search_empty_query(search_api):
    response = search_api.search("")

    assert response.status_code == 200

    result = ObjectList.model_validate(response.json())

    assert isinstance(result.total, int)
    assert isinstance(result.objectIDs, list)


def test_search_offset(search_api):
    first_response = search_api.search(
        "cats",
        offset=0,
        limit=5,
    )

    second_response = search_api.search(
        "cats",
        offset=5,
        limit=5,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first = ObjectList.model_validate(first_response.json())
    second = ObjectList.model_validate(second_response.json())

    assert first.objectIDs
    assert second.objectIDs
    assert first.objectIDs != second.objectIDs
