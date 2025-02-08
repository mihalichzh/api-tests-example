from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectData:
    id: str
    name: str
    comment_count: int
    color: str
    is_shared: bool
    order: int
    is_favorite: bool
    is_inbox_project: bool
    is_team_inbox: bool
    view_style: str
    url: str
    parent_id: Optional[str]
