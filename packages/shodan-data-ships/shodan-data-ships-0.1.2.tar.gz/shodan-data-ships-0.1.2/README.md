# Shodan Data: Ships

A data feed of NMEA messages from open, public ship receivers on the Internet.

OpenAPI Specification: https://ships.data.shodan.io/openapi.json

## Installation

```shell
pip install shodan-data-ships
```

## Quickstart

The library provides both synchronous and asynchronous clients to the Ships datafeed. The easiest way to get started is using the synchronous interface:

```python
from shodan_data_ships.client import Client


client = Client("YOUR SHODAN API KEY")
for msg in client.messages():
    print(msg)
```

## Data Schema

For the latest list of properties that are available please refer to the OpenAPI documentation at:

https://ships.data.shodan.io/docs

Data models are generated from the above JSON schema and are available in the respective ``shodan_data_ships.model.NMEAMessage`` and ``shodan_data_ships.model.Receiver`` classes.

## Asynchronous Client

The library also lets you subscribe to data using ``asyncio``. Simply use the ``shodan_data_ships.client.AsyncClient`` class:

```python
from shodan_data_ships.client import AsyncClient


async def main():
    client = AsyncClient("YOUR SHODAN API KEY")

    async for msg in client.messages():
        print(msg)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
