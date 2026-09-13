import pytest

from models import ObjectList

@pytest.mark.parametrize(
    "keyword",
    [
        "sunflowers",
        "cats",
        "Rembrandt",
    ],
)
def test_search_by_keyword(search_api,keyword: str) -> None:
    response = search_api.search(keyword,limit=5)

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.total > 0, "No search results"
    assert result.object_ids, "Object IDs list is empty"

def test_search_limit(search_api) -> None:
    limit = 10

    response = search_api.search(
        "cats",
        limit=limit,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert len(result.object_ids) == limit, "Unexpected object count"

def test_search_with_filter(search_api) -> None:
    response = search_api.search(
        "cats",
        has_images=True,
        limit=5,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids, "Object IDs list is empty"
    assert len(result.object_ids) <= 5, "Unexpected object count"

def test_search_limit_exceeded(search_api) -> None:
    response = search_api.search(
        "cats",
        limit=501,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert len(result.object_ids) <= 500, "Limit exceeded"

def test_search_max_limit(search_api) -> None:
    response = search_api.search(
        "cats",
        limit=500,
    )

    assert response.status_code == 200, "Unexpected status code"

    result = ObjectList.model_validate(response.json())

    assert len(result.object_ids) == 500, "Unexpected object count"

def test_search_empty_query(search_api) -> None:
    response = search_api.search("")

    assert response.status_code == 200, "Unexpected status code"

    ObjectList.model_validate(response.json())

def test_search_offset(search_api) -> None:
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

    assert first_response.status_code == 200, "Unexpected status code"
    assert second_response.status_code == 200, "Unexpected status code"

    first = ObjectList.model_validate(first_response.json())
    second = ObjectList.model_validate(second_response.json())

    assert first.object_ids, "First result is empty"
    assert second.object_ids, "Second result is empty"
    assert first.object_ids != second.object_ids, "Results are identical"
