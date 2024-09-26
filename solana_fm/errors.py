from typing import Optional, Dict, Any, List


class SolanaFMError(Exception):
    """Base class for errors in SolanaFM API."""

    pass


class HTTPRequestError(SolanaFMError):
    """
    Exception raised for HTTP request errors.

    Attributes:
        message (str): Explanation of the error.
        method (str): The method of the request that caused the error.
        params (list): The parameters of the request that caused the error.
        original_exception (Exception): The original exception raised during the HTTP request.
    """

    def __init__(
        self,
        message: str,
        method: str,
        params: Optional[Dict[str, Any]],
        original_exception: Exception = None,
    ):
        """
        Initialize the HTTPRequestError.

        Args:
            message (str): Explanation of the error.
            method (str): The method of the request that caused the error.
            params (Optional[Dict[str, Any]]): The parameters of the request that caused the error.
            original_exception (Exception, optional): The original exception raised during the HTTP request.
        """
        self.message = message
        self.method = method
        self.params = params
        self.original_exception = original_exception
        super().__init__(message)

    def __str__(self):
        """
        Return a string representation of the HTTPRequestError.
        """
        method_str = f"Method: {self.method}\n" if self.method else ""
        params_str = f"Params: {self.params}\n" if self.params else ""
        exception_str = (
            f"Original Exception: {self.original_exception}\n"
            if self.original_exception
            else ""
        )
        return f"{self.message}\n{method_str}{params_str}{exception_str}"


class NotFoundTransfers(SolanaFMError):
    def __init__(self, params: List[str]):
        self.message = "Not Found Result of Transfers"
        super().__init__(self.message)
