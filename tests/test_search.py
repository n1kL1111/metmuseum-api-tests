import pytest
from api import SearchApi, ObjectsApi
from models import ObjectList, Artwork

@pytest.mark.parametrize(
    ("keyword", "expected_object_id"),
    [
        ("Rembrandt", 728386),
        ("China", 486633),
        ("sunflowers", 397949),
        ("furniture", 347170),
    ],
)
def test_search_by_keyword(search_api: SearchApi, objects_api: ObjectsApi,
                           keyword: str, expected_object_id: int) -> None:
    search_response = search_api.search(keyword, limit=5, title=True)

    assert search_response.status_code == 200, "Неожиданный статус-код"

    search_result = ObjectList.model_validate(search_response.json())

    assert search_result.object_ids, f"Поиск по '{keyword}' не вернул результатов"

    object_response = objects_api.get_object(expected_object_id)

    assert object_response.status_code == 200, f"Неожиданный статус-код при получении объекта {expected_object_id}"

    artwork = Artwork.model_validate(object_response.json())

    assert keyword.lower() in artwork.title.lower(), (f"Ключевое слово '{keyword}'"
                                                      f" отсутствует в названии объекта {expected_object_id}")

    assert expected_object_id in search_result.object_ids, (f"Ожидаемый объект {expected_object_id}"
                                                            f" отсутствует в результатах поиска по '{keyword}'")

@pytest.mark.parametrize(
    "keyword",
    [
        "Rembrandt",
        "Sunflowers",
        "Cat",
        "Japan",
    ],
)
def test_search_is_case_insensitive(search_api: SearchApi, keyword: str) -> None:
    lower_response = search_api.search(keyword.lower())
    upper_response = search_api.search(keyword.upper())
    original_response = search_api.search(keyword)

    assert lower_response.status_code == 200, "Неожиданный статус-код"
    assert upper_response.status_code == 200, "Неожиданный статус-код"
    assert original_response.status_code == 200, "Неожиданный статус-код"

    lower = ObjectList.model_validate(lower_response.json())
    upper = ObjectList.model_validate(upper_response.json())
    original = ObjectList.model_validate(original_response.json())

    assert lower.object_ids, f"Поиск '{keyword.lower()}' не вернул результатов"
    assert upper.object_ids, f"Поиск '{keyword.upper()}' не вернул результатов"
    assert original.object_ids, f"Поиск '{keyword}' не вернул результатов"

    ids_lower = set(lower.object_ids)
    ids_upper = set(upper.object_ids)
    ids_original = set(original.object_ids)

    assert ids_lower == ids_upper == ids_original, f"Регистр влияет на результат для '{keyword}'"

@pytest.mark.parametrize(
    "keyword",
    [
        "qwerty",
        "Картина",
        "!@!#$%",
    ],
)
def test_search_no_results(search_api: SearchApi, keyword: str) -> None:
    response = search_api.search(keyword)

    assert response.status_code == 200, "Неожиданный статус-код"

    data = ObjectList.model_validate(response.json())

    assert data.total == 0, "Ожидалось ноль результатов"
    assert data.object_ids is None, "Ожидалось отсутствие ID объектов"

def test_search_limit(search_api: SearchApi) -> None:
    response = search_api.search("Rembrandt", limit=10)

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids is not None and result.object_ids, "Поиск не вернул результатов"
    assert result.total >= 10, f"Ожидалось не менее 10 совпадений, получено {result.total}"
    assert len(result.object_ids) == 10, f"Ожидалось 10 результатов при limit=10, получено {len(result.object_ids)}"

@pytest.mark.xfail(reason="Баг API: hasImages=true возвращает объекты без изображений", strict=True)
def test_search_with_images_filter(search_api: SearchApi, objects_api: ObjectsApi) -> None:
    response = search_api.search("Rembrandt", has_images=True, limit=100)

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids is not None and result.object_ids, "Поиск не вернул результатов"

    for object_id in result.object_ids:
        object_response = objects_api.get_object(object_id)
        assert object_response.status_code == 200, "Неожиданный статус-код"
        artwork = Artwork.model_validate(object_response.json())
        assert (
            artwork.primary_image
            or artwork.primary_image_small
            or artwork.additional_images
        ), f"У объекта {object_id} нет ни одного изображения (при hasImages=true)"

def test_search_with_is_highlight_filter(search_api: SearchApi, objects_api: ObjectsApi,) -> None:

    response = search_api.search("Rembrandt", is_highlight=True, limit=10)

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids is not None and result.object_ids, "Поиск не вернул результатов"

    for object_id in result.object_ids:
        object_response = objects_api.get_object(object_id)

        assert object_response.status_code == 200, f"Неожиданный статус-код при получении объекта {object_id}"

        artwork = Artwork.model_validate(object_response.json())

        assert artwork.is_highlight is True, (f"Объект {object_id} имеет isHighlight=false"
                                              f", ожидалось True")

def test_search_result_does_not_depend_on_param_order(search_api: SearchApi,) -> None:
    params_order_a = [
        ("q", "sunflowers"),
        ("isHighlight", "true"),
        ("hasImages", "true"),
        ("limit", "20"),
    ]

    params_order_b = list(reversed(params_order_a))

    response_a = search_api.search_raw(params_order_a)
    response_b = search_api.search_raw(params_order_b)

    assert response_a.status_code == 200, "Неожиданный статус-код (порядок A)"
    assert response_b.status_code == 200, "Неожиданный статус-код (порядок B)"

    result_a = ObjectList.model_validate(response_a.json())
    result_b = ObjectList.model_validate(response_b.json())

    assert result_a.total == result_b.total, f"Порядок query-параметров влияет на результат поиска."

    ids_a = set(result_a.object_ids or [])
    ids_b = set(result_b.object_ids or [])

    assert ids_a == ids_b, f"Порядок параметров влияет на состав выдачи."

def test_search_limit_exceeded(search_api: SearchApi) -> None:
    response = search_api.search("Rembrandt", limit=1000)

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids is not None and result.object_ids, "Поиск не вернул результатов"

    assert len(result.object_ids) == 500, "Поиск не ограничился 500"

def test_search_offset(search_api: SearchApi) -> None:
    first_response = search_api.search("Rembrandt",offset=0,limit=10)
    second_response = search_api.search("Rembrandt", offset=10,limit=10)

    assert first_response.status_code == 200, "Неожиданный статус-код (первая страница)"
    assert second_response.status_code == 200, "Неожиданный статус-код (вторая страница)"

    first_result = ObjectList.model_validate(first_response.json())
    second_result = ObjectList.model_validate(second_response.json())

    assert first_result.object_ids is not None, "Первая страница: API вернул null"
    assert second_result.object_ids is not None, "Вторая страница: API вернул null"

    assert len(first_result.object_ids) == 10, (f"Первая страница (offset=0): ожидалось 10 результатов,"
                                                f" получено {len(first_result.object_ids)}")
    assert len(second_result.object_ids) == 10, (f"Вторая страница (offset=10): ожидалось 10 результатов,"
                                                 f" получено {len(second_result.object_ids)}")

    duplicates = set(first_result.object_ids) & set(second_result.object_ids)

    assert not duplicates, f"Страницы поиска (offset=0 и offset=10) содержат дублирующиеся ID: {duplicates}"

def test_search_with_department_filter(search_api: SearchApi, objects_api: ObjectsApi) -> None:

    response = search_api.search("cat", department_id=6, limit=10)

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids is not None and result.object_ids, "Поиск не вернул результатов"

    for object_id in result.object_ids:
        object_response = objects_api.get_object(object_id)

        assert object_response.status_code == 200, f"Неожиданный статус-код при получении объекта {object_id}"

        artwork = Artwork.model_validate(object_response.json())

        assert artwork.department == "Asian Art", (f"Объект {object_id} принадлежит отделу "
                                                   f"{artwork.department} ожидался 'Asian Art' (ID 6)")

def test_search_with_date_range(search_api: SearchApi, objects_api: ObjectsApi) -> None:
    date_begin = 1100
    date_end = 1200

    response = search_api.search("African", date_begin=date_begin, date_end=date_end, limit=10)

    assert response.status_code == 200, "Неожиданный статус-код"

    result = ObjectList.model_validate(response.json())

    assert result.object_ids is not None and result.object_ids, (f"Поиск с диапазоном"
                                                                 f" [{date_begin}, {date_end}] не вернул результатов")

    for object_id in result.object_ids:
        object_response = objects_api.get_object(object_id)
        assert (
            object_response.status_code == 200
        ), f"Неожиданный статус-код при получении объекта {object_id}"
        artwork = Artwork.model_validate(object_response.json())
        assert artwork.object_begin_date is not None, f"У объекта {object_id} не указан objectBeginDate"
        assert artwork.object_end_date is not None, f"У объекта {object_id} не указан objectEndDate"
        assert artwork.object_begin_date >= date_begin, (f"Объект {object_id}: "
                                                         f"objectBeginDate={artwork.object_begin_date}'<' {date_begin}")
        assert artwork.object_end_date <= date_end, (f"Объект {object_id}:"
                                                     f" objectEndDate={artwork.object_end_date} '>' {date_end}")
