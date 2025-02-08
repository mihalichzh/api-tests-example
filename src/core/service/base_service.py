from contextlib import contextmanager

import allure

from src.core.client.api_client import ApiClient


class BaseService:
    def __init__(self, client: ApiClient):
        self.client = client

    @contextmanager
    def _context_step(self, title: str):
        with allure.step(f"[{self.__class__.__name__}] {title}"):
            yield
