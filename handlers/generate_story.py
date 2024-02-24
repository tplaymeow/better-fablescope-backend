import json
import logging
import os
from dataclasses import asdict
from enum import Enum

import requests
from dacite import from_dict, Config

from models.story_response import StoryResponse
from models.tag_ids import TagIDs
from models.tags_category import default_categories
from models.ya_gpt.alternative_status import AlternativeStatus
from models.ya_gpt.completion_options import CompletionOptions
from models.ya_gpt.completion_request import CompletionRequest
from models.ya_gpt.completion_response import CompletionResponse
from models.ya_gpt.message import Message

story_text_prompt = """
Ты - лучший в мире детский писатель. Ты пишешь непревзойденные сказки, которые с упоением читают люди по всему миру.
Твоя задача - на основе присланных тегов, сгенерировать детскую сказку на приблизительно 500 слов.
Сказка должна иметь три акта (Вступление, Кульминация, Завершение).
Каждый акт должен быть абзацем. Перед каждым актом напиши его название (Вступление, Кульминация, Завершение).
В ответ ты всегда присылаешь только саму историю и ничего другого.
"""


def make_text_for_tags(request_data: TagIDs) -> str:
    names: list[str] = []
    for tag_id in request_data.tags:
        for category in default_categories:
            for tag in category.tags:
                if tag.id == tag_id.id:
                    names.append(tag.name)
    return "Теги: " + ", ".join(names)


def perform_ya_gpt_request(access_token: str, request: CompletionRequest) -> CompletionResponse:
    raw_response = requests.post(
        os.environ["YA_GPT_REQUEST_URL"],
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        },
        json=asdict(request)
    )
    return from_dict(CompletionResponse, raw_response.json(), config=Config(cast=[Enum]))


def handler(event, context):
    try:
        request_body_json = json.loads(event["body"])
        request_body_data = from_dict(TagIDs, request_body_json, config=Config(cast=[Enum]))
        tags_text = make_text_for_tags(request_body_data)

        access_token = context.token["access_token"]
        model_uri = os.environ["YA_GPT_MODEL_URI"]

        text_response = perform_ya_gpt_request(
            access_token,
            CompletionRequest(
                model_uri,
                CompletionOptions(stream=False, temperature=0.6, max_tokens=2000),
                messages=[
                    Message("system", story_text_prompt),
                    Message("user", tags_text),
                ]
            )
        )
        if len(text_response.result.alternatives) == 0:
            logging.error("No alternatives")
            return {'statusCode': 400}

        alternative = text_response.result.alternatives[0]
        if alternative.status != AlternativeStatus.ALTERNATIVE_STATUS_FINAL:
            logging.error(f"Wrong alternative status: {alternative.status}")
            return {'statusCode': 400}

        story_text = alternative.message.text

        return {
            'statusCode': 200,
            'body': asdict(
                StoryResponse(
                    story_text
                )
            )
        }

    except Exception as e:
        logging.error(e)
        return {'statusCode': 400}
