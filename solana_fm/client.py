import logging
from typing import Optional, Dict, Any, List
from .http import HTTPClient
from .models import TransfersAmount
from .errors import HTTPRequestError, NotFoundTransfers


class SolanaFM:
    """
    A client for interacting with Solana FM endpoint.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        token: Optional[str] = None,
        proxies: Optional[Dict[str, str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the SolanaClient.

        Args:
            endpoint (str, optional): The URL of the Solana RPC HTTP endpoint. If not provided, the default endpoint will be used.
            proxies (dict, optional): Dictionary mapping protocol or protocol and host to the URL of the proxy.
            logger (Logger, optional): The logger instance to use for logging.
        """
        self.token = token
        self.logger = logger or logging.getLogger(__name__)
        self.http_client = HTTPClient(endpoint=endpoint, proxies=proxies)

    async def get_transfers(self, signatures: List[str]):
        """Retrieve a list of transfers for a given list of transaction hashes.

        transactionHashes- a list of transaction hashes to query for (min: 1, max: 50)
            hydration - a hydration object that contains the following field:
            accountHash - a boolean field to indicate whether to include the account info in the response or not

        """
        try:
            json_response = await self.http_client.send_request(
                method="transfers",
                params={"transactionHashes": signatures},
                token=self.token,
            )
            output = TransfersAmount.from_json(json_response)
            self.logger.info(f"Success(param={signatures})", extra="get_transfers")
            return output
        except NotFoundTransfers as e:
            self.logger.error(e, extra="get_transfers")
            return None
        except HTTPRequestError as e:
            self.logger.error(e, extra="get_transfers")
            return None
