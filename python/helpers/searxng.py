import aiohttp
from python.helpers import runtime

URL = "http://localhost:55510/search"

async def search(query:str):
    return await runtime.call_development_function(_search, query=query)

async def _search(query:str):
    # 设置超时配置：总超时30秒，连接超时10秒
    timeout = aiohttp.ClientTimeout(total=30, connect=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(URL, data={"q": query, "format": "json"}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"SearXNG search failed with status {response.status}: {error_text}")
    except aiohttp.ClientError as e:
        raise Exception(f"SearXNG search connection error: {str(e)}")
    except Exception as e:
        raise Exception(f"SearXNG search error: {str(e)}")
