import allure


def attach_response(response):
    allure.attach(
        response.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        response.text,
        name="Response JSON",
        attachment_type=allure.attachment_type.JSON,
    )