import allure
import pytest
from faker import Faker
from hamcrest import equal_to

from src.core.assertions.helper import assert_that
from src.core.config import Config
from src.core.service.todoist.models.create_project.CreateProjectRequest import (
    CreateProjectRequest,
)
from src.core.service.todoist.models.update_project.UpdateProjectRequest import (
    UpdateProjectRequest,
)
from src.core.service.todoist.models.ViewStyle import ViewStyle
from src.core.service.todoist.todoist_service import TodoistService


class TestProject:
    @pytest.fixture(autouse=True)
    def setup(self, auth_token: str):
        self.todoist_service = TodoistService(
            base_url=Config.api_base_url(),
            api_key=auth_token,
        )
        yield

    @pytest.fixture(autouse=True)
    def cleanup(self, request: pytest.FixtureRequest):
        yield
        prefix = request.node.name
        all_projects = self.todoist_service.get_all_projects().content
        projects_to_delete = [
            project for project in all_projects if prefix in project.name
        ]
        for project in projects_to_delete:
            self.todoist_service.delete_project(project_id=project.id)

    @allure.title("Create a new project")
    def test_create_project(self, request: pytest.FixtureRequest, faker: Faker):
        # prepare project to be created
        item_to_create = CreateProjectRequest(
            name=f"{request.node.name}_{faker.name()}"
        )

        # create new project
        create_project_response = self.todoist_service.create_new_project(
            body=item_to_create
        )

        # check response is successful
        assert_that(
            description="check response is successful",
            obj=create_project_response.status_code,
            matcher=equal_to(200),
        )

        # check new project is in user projects list
        all_user_projects_response = self.todoist_service.get_all_projects()
        assert_that(
            description="user projects contain created project",
            obj=create_project_response.content in all_user_projects_response.content,
            matcher=equal_to(True),
        )

    @allure.title("Delete an existing project")
    def test_delete_project(self, request: pytest.FixtureRequest, faker: Faker):
        # create a project to delete
        created_project = self.todoist_service.create_new_project(
            body=CreateProjectRequest(name=f"{request.node.name}_{faker.name()}")
        ).content

        # delete the project
        delete_response = self.todoist_service.delete_project(
            project_id=created_project.id
        )

        # verify delete response is successful
        assert_that(
            description="check delete response is successful",
            obj=delete_response.status_code,
            matcher=equal_to(204),
        )

        # verify project is no longer in the list
        all_projects_response = self.todoist_service.get_all_projects()
        assert_that(
            description="deleted project should not be in the list",
            obj=created_project not in all_projects_response.content,
            matcher=equal_to(True),
        )

    @allure.title("Get a specific project")
    def test_get_project(self, request: pytest.FixtureRequest, faker: Faker):
        # create a project to get
        created_project = self.todoist_service.create_new_project(
            body=CreateProjectRequest(name=f"{request.node.name}_{faker.name()}")
        ).content

        # get the specific project
        get_response = self.todoist_service.get_project(
            project_id=created_project.id
        )

        # verify get response is successful
        assert_that(
            description="check get response is successful",
            obj=get_response.status_code,
            matcher=equal_to(200),
        )

        # verify project details match
        assert_that(
            description="retrieved project matches created project",
            obj=get_response.content.id,
            matcher=equal_to(created_project.id),
        )
        assert_that(
            description="project name matches",
            obj=get_response.content.name,
            matcher=equal_to(created_project.name),
        )

    @allure.title("Update an existing project")
    def test_update_project(self, request: pytest.FixtureRequest, faker: Faker):
        # create a project to update
        created_project = self.todoist_service.create_new_project(
            body=CreateProjectRequest(name=f"{request.node.name}_{faker.name()}")
        ).content

        # update project with all fields
        new_name = f"Updated_{request.node.name}_{faker.name()}"
        update_request = UpdateProjectRequest(
            name=new_name,
            color="red",
            is_favorite=True,
            view_style=ViewStyle.BOARD
        )
        updated_project = self.todoist_service.update_project(
            project_id=created_project.id,
            body=update_request
        )

        # verify update response is successful
        assert_that(
            description="check update response is successful",
            obj=updated_project.status_code,
            matcher=equal_to(200),
        )

        # verify updated project is in user projects list
        all_user_projects = self.todoist_service.get_all_projects()
        assert_that(
            description="updated project should be in projects list",
            obj=updated_project.content in all_user_projects.content,
            matcher=equal_to(True),
        )
