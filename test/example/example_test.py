import allure
import pytest
from faker import Faker
from hamcrest import equal_to

from src.core.assertions.helper import assert_that
from src.core.config import Config
from src.core.service.todoist.models.create_project.CreateProjectRequest import CreateProjectRequest
from src.core.service.todoist.todoist_service import TodoistService


class TestExample:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.todoist_service = TodoistService(
            base_url=Config.api_base_url(),
            api_key=Config.api_key(),
        )
        yield

    @pytest.fixture(autouse=True)
    def cleanup(self, request: pytest.FixtureRequest):
        yield
        prefix = request.node.name
        all_projects = self.todoist_service.get_all_projects().content
        projects_to_delete = [project for project in all_projects if prefix in project.name]
        for project in projects_to_delete:
            self.todoist_service.delete_project(project_id=project.id)

    @allure.title("Create a new project")
    def test_create_project(self, request: pytest.FixtureRequest, faker: Faker):
        # prepare project to be created
        item_to_create = CreateProjectRequest(name=f"{request.node.name}_{faker.name()}")

        # create new project
        create_project_response = self.todoist_service.create_new_project(body=item_to_create)

        # check response is successful
        assert_that(
            description="check response is successful",
            obj=create_project_response.status_code,
            matcher=equal_to(200)
        )

        # check new project is in user projects list
        all_user_projects_response = self.todoist_service.get_all_projects()
        assert_that(
            description="user projects contain created project",
            obj=create_project_response.content in all_user_projects_response.content,
            matcher=equal_to(True)
        )
