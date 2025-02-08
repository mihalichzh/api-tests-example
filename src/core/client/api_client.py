from dataclasses import dataclass
from http import HTTPMethod
from typing import Optional, Mapping, Any, Union

import allure
import curlify
import requests
import urljoin
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry


@dataclass
class ClientConfig:
    base_url: str
    headers: Optional[Mapping[str, str]] = None
    retry_strategy: Retry = Retry(
        total=3, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504]
    )


class ApiClient:
    def __init__(self, config: ClientConfig):
        self.base_url = config.base_url
        adapter = HTTPAdapter(max_retries=config.retry_strategy)
        self.client = requests.Session()
        self.client.mount("http://", adapter)
        self.client.mount("https://", adapter)
        if config.headers:
            self.client.headers.update(config.headers)

    def request(
            self,
            method: Union[str, HTTPMethod],
            path: str,
            headers: Optional[Mapping[str, str]] = None,
            body: Optional[Any] = None,
    ) -> Response:
        response = self.client.request(
            method=method,
            url=urljoin.url_path_join(self.base_url, path),
            headers=headers,
            data=body,
        )
        self._attach_curlified_request_to_allure(response)
        return response

    def get(
            self,
            path: str,
            headers: Optional[Mapping[str, str]] = None,
            body: Optional[Any] = None,
    ) -> Response:
        return self.request(
            method=HTTPMethod.GET, path=path, headers=headers, body=body
        )

    def post(
            self,
            path: str,
            headers: Optional[Mapping[str, str]] = None,
            body: Optional[Any] = None,
    ) -> Response:
        return self.request(
            method=HTTPMethod.POST, path=path, headers=headers, body=body
        )

    def delete(
            self,
            path: str,
            headers: Optional[Mapping[str, str]] = None,
            body: Optional[Any] = None,
    ) -> Response:
        return self.request(
            method=HTTPMethod.DELETE, path=path, headers=headers, body=body
        )

    @staticmethod
    def _attach_curlified_request_to_allure(response: Response):
        curl_request = curlify.to_curl(response.request)
        allure.attach(
            curl_request, name="Request", attachment_type=allure.attachment_type.TEXT
        )
