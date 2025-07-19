from functools import partial, wraps
from typing import Any, Callable, Literal

from pylms.constants import SECRETS_PATH
from google.oauth2.service_account import Credentials as ServiceCredentials
from apiclient import discovery


def _load_creds() -> ServiceCredentials:
    creds = ServiceCredentials.from_service_account_file(str(SECRETS_PATH))
    return creds


def init_service(
    api: Literal["drive", "forms"],
    version: Literal["v3", "v1"],
) -> Callable:
    creds: ServiceCredentials = _load_creds()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with discovery.build(api, version, credentials=creds) as service:
                mod_func: Callable = partial(func, service=service)
                return mod_func(*args, **kwargs)

        return wrapper

    return decorator
