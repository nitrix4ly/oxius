# oxius

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/oxius.svg?style=flat-square&logo=pypi)](https://pypi.org/project/oxius/)

Ultra-fast, dependency-free async HTTP client for Python. A drop-in alternative to aiohttp with minimal footprint.

## Features

- Fully async with asyncio
- HTTP methods: GET, POST, PUT, DELETE, HEAD, OPTIONS
- SQLite response caching with TTL
- Zero external dependencies
- Clean, simple API

## Installation

```bash
pip install oxius
```

## Quick Start

```python
import asyncio
import oxius

async def main():
    session = oxius.ClientSession()
    response = await session.get("https://catfact.ninja/fact")
    print(response.json())

asyncio.run(main())
```

## Usage

```python
import asyncio
import oxius

async def example():
    session = oxius.ClientSession()

    # GET request
    response = await session.get("https://api.github.com/users/octocat")
    
    # POST with body
    post_response = await session.post(
        "https://httpbin.org/post",
        body='{"key": "value"}',
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status}")
    print(f"Data: {response.json()}")

asyncio.run(example())
```

## API

### Methods
- `session.get(url, headers=None)`
- `session.post(url, headers=None, body=None)`
- `session.put(url, headers=None, body=None)`
- `session.delete(url, headers=None)`
- `session.head(url, headers=None)`
- `session.options(url, headers=None)`

### Response
- `response.status` - HTTP status code
- `response.json()` - Parse JSON response
- `response.text()` - Get response as text
- `response.headers` - Response headers

## License

MIT License
