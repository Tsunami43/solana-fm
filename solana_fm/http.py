from asyncio import sleep
from typing import Optional, Dict, Any, List
from httpx import AsyncClient, ConnectTimeout, ReadTimeout, HTTPError
from .errors import HTTPRequestError


class HTTPClient:
    """
    A utility class for making asynchronous HTTP requests.
    """

    DEFAULT_ENDPOINT = "https://api.solana.fm/v0/"

    def __init__(
        self,
        endpoint: Optional[str] = None,
        proxies: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the HTTPClient.

        Args:
            endpoint (str, optional): The URL of the Solana RPC HTTP endpoint. If not provided, the default endpoint will be used.
            proxies (dict, optional): Dictionary mapping protocol or protocol and host to the URL of the proxy.
        """
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.proxies = proxies

    async def send_request(
        self,
        method: str,
        params: Dict[str, Any],
        token: str = None,
        timeout: int = 30,
        retries: int = 0,
    ) -> dict:
        """
        Send a request to the specified URL asynchronously.

        Args:
            method (str): The method to call.
            params (List[Any]): The parameters to include in the request.

        Returns:
            dict: The JSON response.
        """
        if token is not None:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "ApiKey": token,
            }
        else:
            headers = {"accept": "application/json", "content-type": "application/json"}

        async with AsyncClient(proxies=self.proxies, timeout=timeout) as client:
            try:
                response = await client.post(
                    url=self.endpoint + method, json=params, headers=headers
                )
                response.raise_for_status()
                return response.json()
            except ConnectTimeout as e:
                raise HTTPRequestError(
                    f"ConnectTimeout: {method}", method, params, original_exception=e
                ) from e
            except ReadTimeout as e:
                raise HTTPRequestError(
                    f"ReadTimeout: {method}", method, params, original_exception=e
                ) from e
            except HTTPError as e:
                if e.response.status_code == 429:
                    if retries >= 6:
                        raise HTTPRequestError(
                            f"Retry limit reached ({retries}). {e}",
                            method,
                            params,
                            original_exception=e,
                        ) from e
                    await sleep(2**retries)
                    return await self.send_request(method, params, retries + 1)
                else:
                    raise HTTPRequestError(
                        str(e), method, params, original_exception=e
                    ) from e
            except Exception as e:
                raise HTTPRequestError(
                    f"An unexpected error occurred: {e}",
                    method,
                    params,
                    original_exception=e,
                ) from e
