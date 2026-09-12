import json

import allure
from requests import Response


def attach_request(
    method: str,
    url: str,
    params: dict | None = None,
) -> None:
    request_data = {
        "method": method,
        "url": url,
        "params": params or {},
    }

    allure.attach(
        json.dumps(
            request_data,
            ensure_ascii=False,
            indent=2,
        ),
        name="Request",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_response(response: Response) -> None:
    allure.attach(
        response.url,
        name="Response URL",
        attachment_type=allure.attachment_type.TEXT,
    )

    try:
        response_json = response.json()

        allure.attach(
            json.dumps(
                response_json,
                ensure_ascii=False,
                indent=2,
            ),
            name="Response",
            attachment_type=allure.attachment_type.JSON,
        )

    except ValueError:
        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.TEXT,
        )
