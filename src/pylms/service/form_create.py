from typing import Any

from googleapiclient.http import HttpRequest  # pyright: ignore[reportMissingTypeStubs]

from ..cli_utils import emphasis
from ..errors import eprint
from ..info import print_info
from ..models import Form, FormData
from ._resource import FormResource, FormsService
from .service_init import run_service


def _create_form(
    form_title: str,
    form_name: str,
    *,
    service: FormsService,
) -> Form | None:
    """creates a partially initialized form resource. This form resource is fully initialized by calling the function `setup_form` on the `Form` object returned by this function. The function, however, only returns this `Form` object to success. If the initialization fails, the returned value is None.

    :param form_title: (str): The title of the form as seen on the form by the end user when filling the form out.
    :type form_title: str
    :param form_name: (str): The name of the form as can be seen on the Google Forms webpage.
    :type form_name: str
    :param service: (ResourceAPI): This parameter is automatically filled in due to the application of the `service_init` decorator
    :type service: FormResource

    :return: A `Form` object which contains important metadata on the form resource generated if the function completes successfully. Should it fail, None will be returned
    :rtype: Form | None
    """

    request_body: FormData = {
        "info": {"document_title": form_name, "title": form_title}
    }

    url_key: str = "responderUri"
    form_key: str = "formId"

    form_resource: FormResource = service.forms()
    try:
        create_request: HttpRequest = form_resource.create(body=request_body)
        response: dict[Any, Any] = create_request.execute()  # pyright: ignore[reportUnknownMemberType]
        form_url: str | None = response.get(url_key)  # pyright: ignore[reportUnknownMemberType]
        form_id: str | None = response.get(form_key)  # pyright: ignore[reportUnknownMemberType]
        if form_url is None or form_id is None:
            return None
        print_info(
            f"Form with \nName = {emphasis(form_name)}\nTitle = {emphasis(form_title)}"
        )
        print_info("Created successfully\n")
        return Form(title=form_title, name=form_name, url=form_url, uuid=form_id)
    except Exception as e:
        eprint(
            f"Fatal Error occurred. Please check your Network Connection. Error details: {e}\n"
        )
        return None


def run_create_form(
    form_title: str,
    form_name: str,
) -> Form | None:
    """creates a partially initialized form resource. This form resource is fully initialized by calling the function `run_setup_form` on the `Form` object returned by this function. The function, however, only returns this `Form` object to success. If the initialization fails, the returned value is None.

    :param form_title: (str): The title of the form as shown on the form by the end user when filling the form out.
    :type form_title: str
    :param form_name: (str): The name of the form as can be seen on the Google Forms webpage.
    :type form_name: str

    :return: A `Form` object which contains important metadata on the form resource generated if the function completes successfully. Should it fail, None will be returned
    :rtype: Form | None
    """

    def _run_service(service: FormsService) -> Form | None:
        return _create_form(form_title, form_name, service=service)

    return run_service(
        api="forms",
        version="v1",
        func=_run_service,
    )
