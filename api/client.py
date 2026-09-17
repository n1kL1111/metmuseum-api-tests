import logging
from typing import Any, Iterable, Mapping

import allure
import requests

from utils.allure_helpers import attach_request, attach_response

logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection"

    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def get(
        self,
        endpoint: str,
        version: str = "v1",
        params: Mapping[str, Any] | Iterable[tuple[str, Any]] | None = None,
    ) -> requests.Response:
        url = f"{self.BASE_URL}/{version}/{endpoint}"

        logger.info("GET %s", url)
        if params:
            logger.info("Query params: %s", params)

        with allure.step(f"GET {endpoint}"):
            attach_request(
                method="GET",
                url=url,
                params=params,
            )

            try:
                response = self.session.get(
                    url,
                    params=self._normalize_params(params),
                    timeout=10,
                )
            except requests.RequestException:
                logger.exception("Request failed: %s", url)
                raise

            logger.info(
                "Response: %s %s",
                response.status_code,
                response.url,
            )
            logger.debug("Response body: %s", response.text)

            attach_response(response)

            return response

    @staticmethod
    def _normalize_params(
        params: Mapping[str, Any] | Iterable[tuple[str, Any]] | None,
    ) -> list[tuple[str, str]] | None:

        if params is None:
            return None

        items = params.items() if isinstance(params, Mapping) else params

        normalized: list[tuple[str, str]] = []
        for key, value in items:
            if value is None:
                continue
            if isinstance(value, bool):
                normalized.append((key, "true" if value else "false"))
            else:
                normalized.append((key, str(value)))

        return normalized