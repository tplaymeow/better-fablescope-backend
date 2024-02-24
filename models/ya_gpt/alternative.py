from dataclasses import dataclass

from models.ya_gpt.alternative_status import AlternativeStatus
from models.ya_gpt.message import Message


@dataclass
class Alternative:
    message: Message
    status: AlternativeStatus
