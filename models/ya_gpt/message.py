from dataclasses import dataclass


@dataclass
class Message:
    role: str
    text: str
