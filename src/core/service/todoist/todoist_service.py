from dataclasses import asdict
from typing import List

from src.core.client.api_client import ApiClient, ClientConfig
from src.core.service.base_service import BaseService
from src.core.service.response_container import ResponseContainer
from src.core.service.todoist.models.create_project.CreateProjectRequest import (
    CreateProjectRequest,
)
from src.core.service.todoist.models.ProjectData import ProjectData


class TodoistService(BaseService):
    def __init__(self, base_url: str, api_key: str = None):
        super().__init__(client=ApiClient(config=ClientConfig(base_url=base_url)))
        self.api_key = api_key

    def create_new_project(
        self, body: CreateProjectRequest
    ) -> ResponseContainer[ProjectData]:
        with self._context_step("create new project"):
            response = self.client.post(
                path="/rest/v2/projects",
                body=asdict(body),
                headers={"Authorization": f"Bearer {self.api_key}"}
                if self.api_key
                else None,
            )
            return ResponseContainer(
                status_code=response.status_code,
                headers=dict(**response.headers),
                content=ProjectData(**response.json())
                if response.ok
                else response.text,
            )

    def get_all_projects(self) -> ResponseContainer[List[ProjectData]]:
        with self._context_step("get all projects"):
            response = self.client.get(
                path="/rest/v2/projects",
                headers={"Authorization": f"Bearer {self.api_key}"}
                if self.api_key
                else None,
            )
            return ResponseContainer(
                status_code=response.status_code,
                headers=dict(**response.headers),
                content=[ProjectData(**item) for item in response.json()]
                if response.ok
                else response.text,
            )

    def delete_project(self, project_id: str) -> ResponseContainer[None]:
        response = self.client.delete(
            path=f"/rest/v2/projects/{project_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
            if self.api_key
            else None,
        )
        return ResponseContainer(
            status_code=response.status_code,
            headers=dict(**response.headers),
        )
