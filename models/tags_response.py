from dataclasses import dataclass

from models.tags_category import TagsCategory


@dataclass
class TagsResponse:
    categories: list[TagsCategory]
