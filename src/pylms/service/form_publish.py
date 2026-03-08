from ..cli_utils import emphasis
from ..errors import Result, eprint
from ..info import print_info
from ..models import Form, PublishRequest, PublishSettings, PublishState
from ._resource import FormsService
from .service_init import run_service


def _publish_form(form: Form, service: FormsService) -> Result[Form]:
    """Publishes a Google Form to accept responses.
    
    Sets the form to published state and enables response collection using
    the Google Forms API.
    
    Args:
        form: Form object to publish.
        service: FormsService object for API calls.
        
    Returns:
        Result[Form]: The same Form object on success, error otherwise.
    """
    # Configure form to accept responses
    request = service.forms().setPublishSettings(
        formId=form.uuid,
        body=PublishRequest(
            publishSettings=PublishSettings(
                publishState=PublishState(isAcceptingResponses=True, isPublished=True)
            )
        ).model_dump(exclude_none=True),
    )

    try:
        _ = request.execute()  # pyright: ignore[reportUnknownMemberType]
        print_info(
            f"Form with \nName = {emphasis(form.name)}\nTitle = {emphasis(form.title)}"
        )
        print_info("Published successfully\n")
        return Result.ok(form)
    except Exception as e:
        msg = f"Failed to publish form due to error\nError details: {e}\n"
        eprint(msg)
        return Result.err(msg)


def run_publish_form(form: Form) -> Result[Form]:
    """Publishes a Google Form to accept responses.
    
    Sets the form to published state and enables response collection.
    
    Args:
        form: Form object to publish.
        
    Returns:
        Result[Form]: The same Form object on success, error otherwise.
    """
    # Wrapper to inject FormsService dependency
    def _run_service(service: FormsService) -> Result[Form]:
        return _publish_form(form, service=service)

    return run_service(
        api="forms",
        version="v1",
        func=_run_service,
    )
