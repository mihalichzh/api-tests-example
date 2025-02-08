from dataclasses import dataclass
from typing import Optional

from core.service.todoist.models.ViewStyle import ViewStyle


@dataclass
class CreateProjectRequest:
    name: str
    parent_id: Optional[str] = None
    color: Optional[str] = None
    is_favorite: Optional[bool] = None
    view_style: Optional[ViewStyle] = None
