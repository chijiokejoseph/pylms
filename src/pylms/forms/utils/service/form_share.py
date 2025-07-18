from googleapiclient.http import HttpError, HttpRequest

from pylms.forms.utils.service._form import Form, PermissionsData
from pylms.forms.utils.service._resource import DriveResource
from pylms.forms.utils.service.service_init import init_service


@init_service(api="drive", version="v3")
def share_form(form: Form, email: str, *, service: DriveResource) -> Form | None:
    """
    share_form grants the email specified in the recipient_email argument access to the form whose id is specified in the record argument.

    :param service: ( ResourceAPI ): This parameter is automatically filled in due to the application of the `service_init` decorator
    :type service: DriveResource
    :param form: ( Form ) A Form object that stores the id of the form that is to be shared alongside its url.
    :type form: Form
    :param email: ( str ): An email address that needs to be granted write access.
    :type email: str

    :return: None.
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
