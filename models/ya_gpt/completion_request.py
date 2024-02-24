from dataclasses import dataclass

from models.ya_gpt.completion_options import CompletionOptions
from models.ya_gpt.message import Message


@dataclass
class CompletionRequest:
    model_uri: str
    completion_options: CompletionOptions
    messages: list[Message]
