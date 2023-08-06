from aiohttp import ClientResponse


class BrawlStarsException(Exception):
    """Base exception for the library"""


class HTTPException(BrawlStarsException):
    __slots__ = ("response", "status", "message", "reason", "_data")

    def _from_response(self, response, data):
        self.response = response
        self.status = response.status

        if isinstance(data, dict):
            self.reason = data.get("reason", "Unknown")
            self.message = data.get("message")
        elif isinstance(data, str):
            self.reason = data
            self.message = None
        else:
            self.reason = "Unknown"
            self.message = None

        fmt = "{0.reason} (status code: {0.status})"
        if self.message:
            fmt += ": {0.message}"

        super().__init__(fmt.format(self))

    def __init__(self, response=None, data=None):
        if isinstance(response, ClientResponse):
            self._from_response(response, data)
        else:
            self.response = None
            self.status = 0
            self.reason = None
            self.message = response

            fmt = "Unknown Error Occured: {0}"
            super().__init__(fmt.format(self.message))


class InvalidArgument(HTTPException):
    """
    Thrown when an error status 400 occurs.
    Client provided incorrect parameters for the request.
    Subclass of :exc:`HTTPException`
    """


class InvalidCredentials(HTTPException):
    """Thrown when an error status 403 occurs and the reason is invalid credentials.
    Special Exception thrown when missing/incorrect credentials
    were passed. This is when your email/password pair is incorrect.
    Subclass of :exc:`HTTPException`
    """


class Forbidden(HTTPException):
    """Thrown when an error status 403 occurs.
    API token does not grant access to the requested resource.
    Subclass of :exc:`HTTPException`"""


class NotFound(HTTPException):
    """Thrown when an error status 404 occurs.
    The resource was not found.
    Subclass of :exc:`HTTPException`
    """


class Maintenance(HTTPException):
    """Thrown when an error status 503 occurs.
    Service is temporarily unavailable because of maintenance.
    Subclass of :exc:`HTTPException`
    """


class GatewayError(HTTPException):
    """Thrown when a gateway error occurs. These are either status 502 or 504
    Error code 502: Bad Gateway
    Error code 504: The Gateway has timed-out.
    Subclass of :exc:`HTTPException`
    """
