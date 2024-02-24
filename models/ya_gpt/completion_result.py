from dataclasses import dataclass

from models.ya_gpt.alternative import Alternative


@dataclass
class CompletionResult:
    alternatives: list[Alternative]
