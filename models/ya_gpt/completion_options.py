from dataclasses import dataclass


@dataclass
class CompletionOptions:
    stream: bool
    temperature: float
    max_tokens: int
