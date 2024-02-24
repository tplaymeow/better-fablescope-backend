from dataclasses import asdict

from models.tags_category import default_categories
from models.tags_response import TagsResponse


def handler(event, context):
    return {
        'statusCode': 200,
        'body': asdict(
            TagsResponse(
                default_categories
            )
        )
    }
