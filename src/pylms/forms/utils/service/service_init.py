from typing import Callable, Literal

from pylms.constants import SECRETS_PATH
from google.oauth2.service_account import Credentials as ServiceCredentials
from apiclient import discovery
from pylms.forms.utils.service._resource import FormResource, DriveResource


def _load_creds() -> ServiceCredentials:
    """
    :return: (ServiceCredentials) - The credentials loaded from the file at SECRETS_PATH
    :rtype: ServiceCredentials
    """
    creds = ServiceCredentials.from_service_account_file(str(SECRETS_PATH))
    return creds


def run_service[T: FormResource | DriveResource, K](
    api: Literal["drive", "forms"],
    version: Literal["v3", "v1"],
    func: Callable[[T], K],
) -> K:
    """
    Creates a Google API client from the credentials stored in the path specified by SECRETS_PATH, and calls the provided function with the created service as an argument.

    :param api: The API to be used. Must be "drive" or "forms".
    :param version: The version of the API to use. Must be "v3" or "v1".
    :param func: The function to be called with the created service as an argument.

    :return: The result of calling the provided function with the created service as an argument.
    """
    creds: ServiceCredentials = _load_creds()
    with discovery.build(api, version, credentials=creds) as service:
        return func(service)
