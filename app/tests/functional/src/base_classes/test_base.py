import aiohttp
from app.tests.functional.settings import ServiceParams


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
        self.api_url = ServiceParams().url()

        self.headers = None

        self.endpoint = self.api_url + endpoint
        self.method = method
        self.params = params
        self.json = json
        self.data = data
        self.expected_status = expected_status
        self.expected_response = expected_response
        self.expected_detail = expected_detail

        self.response: aiohttp.ClientResponse | None = None
        self.response_json: dict | None = None

    async def make_request(self):
        async with aiohttp.ClientSession() as session:
            self.response: aiohttp.ClientResponse = await session.request(
                url=self.endpoint,
                method=self.method,
                params=self.params,
                json=self.json,
                data=self.data,
                headers=self.headers,
            )

    async def assert_status_code(self):
        assert self.response.status == self.expected_status, self.response.text

    async def assert_expected_detail(self):
        assert self.response_json["detail"] == self.expected_detail, "expected_detail"

    async def assert_expected_json(self):
        assert self.response_json == self.expected_response, "expected_response"

    async def assert_response(self) -> None:
        self.response_json = await self.response.json()

        await self.assert_status_code()

        if self.expected_detail is not None:
            await self.assert_expected_detail()

        if self.response.status // 100 == 2 and self.expected_response is not None:
            await self.assert_expected_json()

    async def perform(self) -> None:
        await self.make_request()
        await self.assert_response()
