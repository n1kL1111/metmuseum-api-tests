TEST_METADATA = {
    "test_get_artwork": {
        "title": "Получение произведения искусства по ID",
        "description": "Проверка получения существующего произведения искусства",
    },
    "test_get_nonexistent_artwork": {
        "title": "Получение несуществующего произведения",
        "description": "Проверка обработки запроса с несуществующим ID",
    },
    "test_get_objects": {
        "title": "Получение списка произведений",
        "description": "Проверка получения списка идентификаторов произведений",
    },
    "test_search_by_keyword": {
        "title": "Поиск произведений по ключевому слову",
        "description": "Проверка поиска произведений по ключевому слову",
    },
    "test_search_limit": {
        "title": "Ограничение количества результатов поиска",
        "description": "Проверка параметра limit",
    },
    "test_search_with_filter": {
        "title": "Поиск с фильтром наличия изображений",
        "description": "Проверка выполнения поиска с параметром hasImages",
    },
    "test_search_empty_query": {
        "title": "Поиск с пустым запросом",
        "description": "Проверка обработки пустого поискового запроса",
    },
    "test_search_offset": {
        "title": "Пагинация результатов поиска",
        "description": "Проверка параметра offset",
    },
}


FILE_NAMES = {
    "test_objects.py": "Objects API",
    "test_search.py": "Search API",
}