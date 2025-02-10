from dataclasses import dataclass
from typing import Optional

from src.core.service.todoist.models.ViewStyle import ViewStyle


@dataclass
class UpdateProjectRequest:
    name: Optional[str] = None
    color: Optional[str] = None
    is_favorite: Optional[bool] = None
    view_style: Optional[ViewStyle] = None 