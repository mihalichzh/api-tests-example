from dataclasses import asdict
from typing import List

from src.core.client.api_client import ApiClient, ClientConfig
from src.core.service.base_service import BaseService
from src.core.service.response_container import ResponseContainer
from src.core.service.todoist.models.create_project.CreateProjectRequest import (
    CreateProjectRequest,
)
from src.core.service.todoist.models.ProjectData import ProjectData
from src.core.service.todoist.models.update_project.UpdateProjectRequest import (
    UpdateProjectRequest,
)


class TodoistService(BaseService):
    def __init__(self, base_url: str, api_key: str = None):
        """
        Initialize TodoistService
        
        Args:
            base_url (str): Base URL for the Todoist API
            api_key (str, optional): API key for authentication. Defaults to None
        """
        super().__init__(client=ApiClient(config=ClientConfig(base_url=base_url)))
        self.api_key = api_key

    def create_new_project(
        self, body: CreateProjectRequest
    ) -> ResponseContainer[ProjectData]:
        """
        Create a new Todoist project
        
        Args:
            body (CreateProjectRequest): The project creation request data
            
        Returns:
            ResponseContainer[ProjectData]: Response containing the created project data
        """
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
        """
        Retrieve all projects for the authenticated user
        
        Returns:
            ResponseContainer[List[ProjectData]]: List of all projects
        """
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
        """
        Delete a specific project by ID
        
        Args:
            project_id (str): The ID of the project to delete
            
        Returns:
            ResponseContainer[None]: Response indicating deletion status
        """
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

    def get_project(self, project_id: str) -> ResponseContainer[ProjectData]:
        """
        Get a specific project by ID
        
        Args:
            project_id (str): The ID of the project to retrieve
            
        Returns:
            ResponseContainer[ProjectData]: Response containing the project data
        """
        response = self.client.get(
            path=f"/rest/v2/projects/{project_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
            if self.api_key
            else None,
        )
        return ResponseContainer(
            status_code=response.status_code,
            headers=dict(**response.headers),
            content=ProjectData(**response.json()) if response.ok else response.text,
        )

    def update_project(
            self,
            project_id: str,
            body: UpdateProjectRequest
    ) -> ResponseContainer[ProjectData]:
        """
        Update an existing project
        
        Args:
            project_id (str): The ID of the project to update
            body (UpdateProjectRequest): The project update data
            
        Returns:
            ResponseContainer[ProjectData]: Response containing the updated project data
        """
        response = self.client.post(
            path=f"/rest/v2/projects/{project_id}",
            body=asdict(body),
            headers={"Authorization": f"Bearer {self.api_key}"}
            if self.api_key
            else None,
        )
        return ResponseContainer(
            status_code=response.status_code,
            headers=dict(**response.headers),
            content=ProjectData(**response.json()) if response.ok else response.text,
        )
