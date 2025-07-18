from typing import Any

from google.auth.exceptions import TransportError
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest

from pylms.models import ContentBody
from pylms.models import Form
from pylms.forms.utils.service._resource import FormResource
from pylms.forms.utils.service.service_init import init_service


@init_service(api="forms", version="v1")
def setup_form(
    form: Form, form_content: ContentBody, *, service: FormResource
) -> Form | None:
    """completes the initialization of a Google form using the `Form` object returned from the `create_form` function which stores the url and form id of the created form.
    the initialization is completed by updating the form's contents using the argument passed in through the parameter `form_content`. just like `create_form`, the `Form` object passed in is returned if the operation is successful else None is returned.

    :param service: (FormResource): This parameter is automatically filled in due to the application of the `init_service` decorator
    :type service: FormResource
    :param form: (Form): a `Form` object, generated by the `create_form` function that stores the metadata of the partially initialized form whose initialization is completed when this function `setup_form` runs successfully.
    :type form: form
    :param form_content: (ContentBody): A typed dictionary with a single key `requests` which stores a list of a nested structure containing typed dictionaries. in other words, the structure of ContentBody could be broken down as

        - ContentBody
            - "requests": list[Content]

        - Content: is a Pydantic Model whose contents can be filled using completion context menus

    :type form_content: ContentBody

    :return: a `Form` object which is identical to the one passed in through the `form` argument and is returned if the function completes successfully else None is returned.
    :rtype: form | None
    """

    form_id: str = form.uuid
    form_resource: FormResource = service.forms()
    request_body: dict[str, Any] = form_content.model_dump(exclude_none=True)
    try:
        request: HttpRequest = form_resource.batchUpdate(
            formId=form_id, body=request_body
        )
        request.execute()
        print(
            f"\nForm with name={form.name}, title={form.title} and url={form.url} setup successfully.\n"
        )
        return form
    except (HttpError, TransportError) as e:
        print(f"\nFatal error occurred while updating form. Error encountered is {e}\n")
        return None
