from requests import Response

from .client import ApiClient


class SearchApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def search(
        self,
        q: str,
        is_highlight: bool | None = None,
        title: bool | None = None,
        tags: bool | None = None,
        department_id: int | None = None,
        is_on_view: bool | None = None,
        artist_or_culture: bool | None = None,
        medium: bool | None = None,
        has_images: bool | None = None,
        geo_location: str | None = None,
        date_begin: int | None = None,
        date_end: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Response:
        params = {
            "q": q,
            "isHighlight": is_highlight,
            "title": title,
            "tags": tags,
            "departmentId": department_id,
            "isOnView": is_on_view,
            "artistOrCulture": artist_or_culture,
            "medium": medium,
            "hasImages": has_images,
            "geoLocation": geo_location,
            "dateBegin": date_begin,
            "dateEnd": date_end,
            "offset": offset,
            "limit": limit,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        return self.client.get(
            "search",
            version="v1.1",
            params=params,
        )

    def search_raw(self, params: list[tuple[str, str]]) -> Response:
        return self.client.get(
            "search",
            version="v1.1",
            params=params,
        )
