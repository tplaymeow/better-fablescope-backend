from dataclasses import dataclass

from models.tag_id import TagID


@dataclass
class TagIDs:
    tags: list[TagID]
