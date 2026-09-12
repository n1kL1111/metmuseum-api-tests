import logging

import requests


logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection"

    def __init__(self, session: requests.Session):
        self.session = session

    def get(
        self,
        endpoint: str,
        *,
        version: str = "v1",
        params: dict | None = None,
    ):
        url = f"{self.BASE_URL}/{version}/{endpoint}"

        logger.info("GET %s", url)

        if params:
            logger.info("Query params: %s", params)

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=10,
            )

            logger.info(
                "Response: %s %s",
                response.status_code,
                response.url,
            )

            logger.debug("Response body: %s", response.text)

            return response

        except requests.RequestException:
            logger.exception("Request failed: %s", url)
            raise
