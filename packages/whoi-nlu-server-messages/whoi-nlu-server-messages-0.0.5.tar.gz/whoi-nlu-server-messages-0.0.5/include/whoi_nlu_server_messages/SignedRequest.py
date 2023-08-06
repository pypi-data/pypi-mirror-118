import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class SignedRequest(CBorMessage):
    key: str
    payload: bytes
