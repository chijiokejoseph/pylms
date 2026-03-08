from typing import Any

from googleapiclient.http import HttpRequest  # pyright: ignore[reportMissingTypeStubs]

from ..cli_utils import emphasis
from ..errors import Result, eprint
from ..info import print_info
from ..models import Form, FormData
from ._resource import FormResource, FormsService
from .service_init import run_service


def _create_form(
    form_title: str,
    form_name: str,
    *,
    service: FormsService,
) -> Result[Form]:
    """Creates a partially initialized Google Form resource.
    
    Creates a new form with the specified title and name using the Google Forms API.
    The form must be further initialized with run_setup_form to add questions and content.
    
    Args:
        form_title: The title displayed on the form to end users.
        form_name: The name of the form as shown in Google Forms.
        service: FormsService object for API calls.
        
    Returns:
        Result[Form]: Form object with metadata (title, name, url, uuid) on success, error otherwise.
    """

    # Prepare form creation request body
    request_body: FormData = {
        "info": {"document_title": form_name, "title": form_title}
    }

    url_key: str = "responderUri"
    form_key: str = "formId"

    # Create form via Google Forms API
    form_resource: FormResource = service.forms()
    try:
        create_request: HttpRequest = form_resource.create(body=request_body)
        response: dict[Any, Any] = create_request.execute()  # pyright: ignore[reportUnknownMemberType]
        form_url: str | None = response.get(url_key)  # pyright: ignore[reportUnknownMemberType]
        form_id: str | None = response.get(form_key)  # pyright: ignore[reportUnknownMemberType]
        
        # Validate response contains required fields
        if form_url is None or form_id is None:
            msg = "Form creation failed: missing URL or ID"
            eprint(msg)
            return Result.err(msg)
        
        print_info(
            f"Form with \nName = {emphasis(form_name)}\nTitle = {emphasis(form_title)}"
        )
        print_info("Created successfully\n")
        return Result.ok(Form(title=form_title, name=form_name, url=form_url, uuid=form_id))
    except Exception as e:
        msg = f"Fatal Error occurred. Please check your Network Connection. Error details: {e}\n"
        eprint(msg)
        return Result.err(msg)


def run_create_form(
    form_title: str,
    form_name: str,
) -> Result[Form]:
    """Creates a partially initialized Google Form resource.
    
    Creates a new form with the specified title and name. The form must be
    further initialized with run_setup_form to add questions and content.
    
    Args:
        form_title: The title displayed on the form to end users.
        form_name: The name of the form as shown in Google Forms.
        
    Returns:
        Result[Form]: Form object with metadata (title, name, url, uuid) on success, error otherwise.
    """
    # Wrapper to inject FormsService dependency
    def _run_service(service: FormsService) -> Result[Form]:
        return _create_form(form_title, form_name, service=service)

    return run_service(
        api="forms",
        version="v1",
        func=_run_service,
    )
