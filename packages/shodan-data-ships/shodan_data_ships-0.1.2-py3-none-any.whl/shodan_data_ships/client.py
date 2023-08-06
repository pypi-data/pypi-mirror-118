from httpx import Client as HttpClient, AsyncClient as AsyncHttpClient
from pydantic import parse_obj_as
from typing import Generator, List

from .model import NMEAMessage, Receiver


API_URL = "https://ships.data.shodan.io"


class Client:

    api_key: str = None

    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def messages(self) -> Generator[NMEAMessage, None, None]:
        client = HttpClient()
        with client.stream("GET", f"{API_URL}/api/messages?key={self.api_key}") as response:
            for line in response.iter_lines():
                yield NMEAMessage.parse_raw(line)
    
    def receivers(self) -> List[Receiver]:
        client = HttpClient()
        response = client.get(f"{API_URL}/api/receivers?key={self.api_key}")
        return parse_obj_as(List[Receiver], response.json())


class AsyncClient(Client):

    async def messages(self):
        async with AsyncHttpClient() as client:
            async with client.stream("GET", f"{API_URL}/api/messages?key={self.api_key}") as response:
                async for line in response.aiter_lines():
                    yield NMEAMessage.parse_raw(line)

    async def receivers(self):
        async with AsyncHttpClient() as client:
            response = await client.get(f"{API_URL}/api/receivers?key={self.api_key}")
            return parse_obj_as(List[Receiver], response.json())
