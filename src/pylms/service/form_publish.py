from ..errors import eprint
from ..info import print_info
from ..models import Form, PublishRequest, PublishSettings, PublishState
from ._resource import FormsService
from .service_init import run_service


def _publish_form(form: Form, service: FormsService) -> Form | None:
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
            f"Form with name={form.name} and title={form.title} published successfully\n"
        )
        return form
    except Exception as e:
        eprint(f"Failed to publish form due to error\nError details: {e}\n")
        return None


def run_publish_form(form: Form) -> Form | None:
    def _run_service(service: FormsService) -> Form | None:
        return _publish_form(form, service=service)

    return run_service(
        api="forms",
        version="v1",
        func=_run_service,
    )
