from pylms.forms.retrieve_form_api.cds_form import retrieve_cds_form
from pylms.forms.retrieve_form_api.class_form import retrieve_class_form
from pylms.forms.retrieve_form_api.enums import ClassType, RetrieveType
from pylms.forms.retrieve_form_api.save_retrieve import save_retrieve
from pylms.forms.retrieve_form_api.update_form import retrieve_update_form

__all__ = [
    "retrieve_update_form",
    "retrieve_cds_form",
    "retrieve_class_form",
    "save_retrieve",
    "ClassType",
    "RetrieveType",
]


"""Provides functions for retrieving forms from Google Forms.

The functions in this module are used to retrieve a form and its responses
from Google Forms. The functions are:

- `retrieve_cds_form`: Retrieves a CDS form and its responses.
- `retrieve_class_form`: Retrieves a class form and its responses.
- `retrieve_update_form`: Retrieves an update form and its responses.
- `save_retrieve`: Saves the retrieved form and responses to a file.

The module also contains the following classes:

- `ClassType`: An enumeration for the type of class form.
- `RetrieveType`: An enumeration for the type of form to retrieve.

"""
