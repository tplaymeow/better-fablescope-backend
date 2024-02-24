from dataclasses import dataclass

from models.ya_gpt.completion_result import CompletionResult


@dataclass
class CompletionResponse:
    result: CompletionResult
