from typing import Optional

import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage


@dataclasses.dataclass
class NetworkDescription(CBorMessage):
    data_hostname: Optional[str] = None
    data_port: Optional[int] = None
    control_hostname: Optional[str] = None
    control_port: Optional[int] = None
    speech_to_text_hostname: Optional[str] = None
    speech_to_text_port: Optional[int] = None
    h2sl_hostname: Optional[str] = None
    h2sl_port: Optional[int] = None
