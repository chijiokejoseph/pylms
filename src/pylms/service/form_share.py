from googleapiclient.http import (  # pyright: ignore[reportMissingTypeStubs]
    HttpRequest,
)

from ..cli_utils import emphasis
from ..errors import Result, eprint
from ..info import printpass
from ..models import Form, PermissionsData
from ._resource import DriveResource
from .service_init import run_service


def _share_form(form: Form, gmail: str, *, service: DriveResource) -> Result[Form]:
    """Grants write access to a Gmail address for a form.
    
    Uses Google Drive API to share the form file with the specified Gmail address,
    granting writer permissions.
    
    Args:
        form: Form object to share.
        gmail: Gmail address to grant write access.
        service: DriveResource object for API calls.
        
    Returns:
        Result[Form]: The same Form object on success, error otherwise.
    """
    # Configure writer permission for the Gmail address
    user_permission: PermissionsData = {
        "type": "user",
        "role": "writer",
        "emailAddress": gmail,
    }
    
    try:
        # Create permission via Google Drive API
        drive_resource: DriveResource = service.permissions()
        share_request: HttpRequest = drive_resource.create(
            fileId=form.uuid, body=user_permission
        )
        share_request.execute()  # pyright: ignore[reportUnknownMemberType]
        printpass(
            f"Success, form {emphasis(form.name)} has been shared to {gmail}. SUCCESS\n"
        )
        return Result.ok(form)
    except Exception as e:
        msg = f"Fatal error occurred while sharing form {emphasis(form.name)} with {gmail}. Error encountered is {e}. ERROR\n"
        eprint(msg)
        return Result.err(msg)


def run_share_form(form: Form, gmail: str) -> Result[Form]:
    """Grants write access to a Gmail address for a form.
    
    Uses Google Drive API to share the form with the specified Gmail address.
    
    Args:
        form: Form object to share.
        gmail: Gmail address to grant write access.
        
    Returns:
        Result[Form]: The same Form object on success, error otherwise.
    """
    # Wrapper to inject DriveResource dependency
    def _run_service(service: DriveResource) -> Result[Form]:
        return _share_form(form, gmail, service=service)

    return run_service(
        api="drive",
        version="v3",
        func=_run_service,
    )


def run_share_form_multiple(form: Form, gmails: list[str]) -> Result[Form]:
    """Grants write access to multiple Gmail addresses for a form.
    
    Shares the form with all specified Gmail addresses. If any sharing operation
    fails, returns error immediately.
    
    Args:
        form: Form object to share.
        gmails: List of Gmail addresses to grant write access.
        
    Returns:
        Result[Form]: The same Form object if all shares succeed, error otherwise.
    """
    # Share with each Gmail address sequentially
    for gmail in gmails:
        result = run_share_form(form, gmail)
        if result.is_err():
            return result
    
    return Result.ok(form)
