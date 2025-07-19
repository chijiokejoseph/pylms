from typing import Any, Protocol, Self
from abc import abstractmethod

from googleapiclient.http import HttpRequest

from pylms.models import FormData, PermissionsData


class ResponseResource(Protocol):
    # noinspection PyPep8Naming
    @abstractmethod
    def get(self, *, formId: str, responseId: str) -> object:
        pass

    # noinspection PyPep8Naming
    @abstractmethod
    def list(
        self,
        *,
        formId: str,
        filter: str | None = None,
        pageSize: int = 5000,
    ) -> HttpRequest:
        """
        Currently, the only supported filters are: * timestamp > *N* which means to get all form responses submitted after (but not at) timestamp *N*. * timestamp >= *N* which means to get all form responses submitted at and after timestamp *N*. For both supported filters, timestamp must be formatted in RFC3339 UTC "Zulu" format. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        :param formId: ( str ): The formId from a previously generated form.
        :type formId: str
        :param filter: ( str | None, optional ): A filter to determine which responses to return based on their timestamp. Defaults to None.
        :type filter: str | None
        :param pageSize: ( int, optional ): The number of responses to return per page. Defaults to 5000.
        :type pageSize: int

        :return: ( HttpRequest ): A request which when executed returns the responses from the selected form.
        :rtype: HttpRequest
        """
        pass


class FormResource(Protocol):
    @abstractmethod
    def create(self, *, body: FormData) -> HttpRequest:
        pass

    @abstractmethod
    def forms(self) -> Self:
        pass

    @abstractmethod
    def responses(self) -> ResponseResource:
        pass

    # noinspection PyPep8Naming
    @abstractmethod
    def get(self, *, formId: str) -> HttpRequest:
        pass

    # noinspection PyPep8Naming
    @abstractmethod
    def batchUpdate(self, *, formId: str, body: dict[str, Any]) -> HttpRequest:
        pass


class DriveResource(Protocol):
    @abstractmethod
    def permissions(self) -> Self:
        pass

    # noinspection PyPep8Naming
    @abstractmethod
    def create(self, *, fileId: str, body: PermissionsData) -> HttpRequest:
        pass
