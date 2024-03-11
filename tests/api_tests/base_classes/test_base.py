from fastapi.testclient import TestClient

from app.main import app


class TestApiBase:
    __test__ = False

    def __init__(
        self,
        endpoint: str,
        method: str,
        expected_status: int,
        params: dict | None = None,
        json: dict | None = None,
        data: dict | None = None,
        expected_response: dict | None = None,
        expected_detail: str | None = None,
    ):
        self.client = TestClient(app=app)
        self.api_url = "http://127.0.0.1:8000"

        self.headers = None

        self.endpoint = self.api_url + endpoint
        self.method = method
        self.params = params
        self.json = json
        self.data = data
        self.expected_status = expected_status
        self.expected_response = expected_response
        self.expected_detail = expected_detail

        self.response = None

    def make_request(self):
        self.response = self.client.request(
            url=self.endpoint,
            method=self.method,
            params=self.params,
            json=self.json,
            data=self.data,
            headers=self.headers,
        )

    def assert_status_code(self):
        assert self.response.status_code == self.expected_status, self.response.text

    def assert_expected_detail(self):
        assert self.response.json()["detail"] == self.expected_detail, "expected_detail"

    def assert_expected_json(self):
        assert self.response.json() == self.expected_response, "expected_response"

    def assert_response(self) -> None:
        self.assert_status_code()

        if self.expected_detail is not None:
            self.assert_expected_detail()

        if self.response.status_code // 100 == 2 and self.expected_response is not None:
            self.assert_expected_json()

    def perform(self) -> None:
        self.make_request()
        self.assert_response()
