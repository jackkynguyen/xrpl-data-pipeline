from dataclasses import dataclass, field
from typing import Optional, Union, cast

from xrpl.asyncio.clients import Client, XRPLRequestFailureException
from xrpl.models.requests.request import Request, RequestMethod
from xrpl.models.utils import require_kwargs_on_init


async def get_latest_validated_ledger_sequence(client: Client) -> int:
    """
    Returns the sequence number of the latest validated ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest validated ledger.

    Raises:
        XRPLRequestFailureException: if the rippled API call fails.
    """
    response = await client.request_impl(Ledger(ledger_index="validated"))
    if response.is_successful():
        return cast(int, response.result["ledger_index"])

    raise XRPLRequestFailureException(response.result)


@require_kwargs_on_init
@dataclass(frozen=True)
class Ledger(Request):
    """
    Retrieve information about the public ledger.
    `See ledger <https://xrpl.org/ledger.html>`_
    """

    method: RequestMethod = field(default=RequestMethod.LEDGER, init=False)
    ledger_hash: Optional[str] = None
    ledger_index: Optional[Union[str, int]] = None
    transactions: bool = False
    expand: bool = False
    owner_funds: bool = False
    binary: bool = False
    queue: bool = False
