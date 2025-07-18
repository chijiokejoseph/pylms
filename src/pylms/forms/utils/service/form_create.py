from google.auth.exceptions import TransportError
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest

from pylms.forms.utils.service._form import Form, FormData
from pylms.forms.utils.service._resource import FormResource
from pylms.forms.utils.service.service_init import init_service


@init_service(api="forms", version="v1")
def create_form(
    form_title: str,
    form_name: str,
    *,
    service: FormResource,
) -> Form | None:
    """creates a partially initialized form resource. This form resource is fully initialized by calling the function `setup_form` on the `Form` object returned by this function. The function, however, only returns this `Form` object to success. If the initialization fails, the returned value is None.

    :param form_title: (str): The title of the form as shown on the Google Forms webpage.
    :type form_title: str
    :param form_name: (str): The title of the form as seen on the form by the end user when filling the form out.
    :type form_name: str
    :param service: (ResourceAPI): This parameter is automatically filled in due to the application of the `service_init` decorator
    :type service: FormResource

    :return: A `Form` object which contains important metadata on the form resource generated if the function completes successfully. Should it fail, None will be returned
    :rtype: Form | None
    """

    request_body: FormData = {
        "info": {"document_title": form_name, "title": form_title}
    }

    url_key: str = "responderUri"
    form_key: str = "formId"

    form_resource: FormResource = service.forms()
    try:
        create_request: HttpRequest = form_resource.create(body=request_body)
        response: dict = create_request.execute()
        form_url: str | None = response.get(url_key)
        form_id: str | None = response.get(form_key)
        if form_url is None or form_id is None:
            return None
        print(
            f"\nForm with name={form_name} and title={form_title} created successfully\n"
        )
        return Form(title=form_title, name=form_name, url=form_url, uuid=form_id)
    except (HttpError, TransportError) as e:
        print(
            f"\nFatal Error occurred. Please check your Network Connection. Error details: {e}\n"
        )
        return None
