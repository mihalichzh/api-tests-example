from typing import Any

import allure
import hamcrest
from hamcrest.core.matcher import Matcher


def assert_that(description: str, obj: Any, matcher: Matcher):
    with allure.step(f"[Assert] {description}"):
        hamcrest.assert_that(obj, matcher)
