from googleapiclient.http import HttpError, HttpRequest

from pylms.models import Form, PermissionsData
from pylms.forms.utils.service._resource import DriveResource
from typing import cast
from pylms.forms.utils.service.service_init import run_service


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
        share_request.execute()
        print(f"\nSuccess, form {form.name} has been shared to {email}.", "SUCCESS\n")
        return form
    except (HttpError, TimeoutError) as e:
        print(
            f"\nFatal error occurred while sharing {form.url} with {email}. Error encountered is {e}",
            "ERROR\n",
        )
        return None


def run_share_form(form: Form, email: str) -> Form | None:
    """
    Grants write access to a specified email for the given form using the Google Drive API.

    :param form: (Form) - A `Form` object that stores the id and url of the form to be shared.
    :param email: (str) - The email address to grant write access to the form.

    :return: (Form | None) - The `Form` object if the sharing operation is successful, else None.
    """
    return run_service(
        api="drive",
        version="v3",
        func=lambda service: _share_form(
            form, email, service=cast(DriveResource, service)
        ),
    )
