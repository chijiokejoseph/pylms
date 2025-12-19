from googleapiclient.http import (  # pyright: ignore[reportMissingTypeStubs]
    HttpRequest,
)

from ..errors import eprint
from ..info import printpass
from ..models import Form, PermissionsData
from ._resource import DriveResource
from .service_init import run_service


def _share_form(form: Form, email: str, *, service: DriveResource) -> Form | None:
    """
    Grants write access to a specified email for the given form using the Google Drive API.

    :param form: (Form) - A Form object that stores the id of the form that is to be shared alongside its url.
    :param email: (str) - An email address that needs to be granted write access.
    :param service: (DriveResource) - DriveResource object that provides the permissions() method to create a permission for the form file specified by form.uuid

    :return: The `Form` object if the sharing operation is successful, else None.
    :rtype: Form | None
    """

    user_permission: PermissionsData = {
        "type": "user",
        "role": "writer",
        "emailAddress": email,
    }
    try:
        drive_resource: DriveResource = service.permissions()
        share_request: HttpRequest = drive_resource.create(
            fileId=form.uuid, body=user_permission
        )
        share_request.execute()  # pyright: ignore[reportUnknownMemberType]
        printpass(f"Success, form {form.name} has been shared to {email}. SUCCESS\n")
        return form
    except Exception as e:
        eprint(
            f"Fatal error occurred while sharing {form.url} with {email}. Error encountered is {e}. ERROR\n",
        )
        return None


def run_share_form(form: Form, email: str) -> Form | None:
    """
    Grants write access to a specified email for the given form using the Google Drive API.

    :param form: (Form) - A `Form` object that stores the id and url of the form to be shared.
    :param email: (str) - The email address to grant write access to the form.

    :return: (Form | None) - The `Form` object if the sharing operation is successful, else None.
    """

    def _run_service(service: DriveResource) -> Form | None:
        return _share_form(form, email, service=service)

    return run_service(
        api="drive",
        version="v3",
        func=_run_service,
    )
