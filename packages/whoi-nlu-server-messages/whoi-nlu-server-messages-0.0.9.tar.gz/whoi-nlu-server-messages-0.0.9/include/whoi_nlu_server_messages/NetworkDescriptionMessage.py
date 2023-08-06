from typing import Optional

import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class NetworkDescriptionMessage(CBorMessage):
    control_hostname: Optional[str] = None
    control_port: int = 0
    data_hostname: Optional[str] = None
    data_port: int = 0
    speech_to_text_hostname: Optional[str] = None
    speech_to_text_port: int = 0
    h2sl_hostname: Optional[str] = None
    h2sl_port: int = 0
