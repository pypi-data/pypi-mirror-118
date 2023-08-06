from typing import Optional

import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class NetworkDescriptionMessage(CBorMessage):
    data_hostname: Optional[str] = None
    data_port: Optional[int] = 0
    control_hostname: Optional[str] = None
    control_port: Optional[int] = 0
    speech_to_text_hostname: Optional[str] = None
    speech_to_text_port: Optional[int] = 0
    h2sl_hostname: Optional[str] = None
    h2sl_port: Optional[int] = 0
