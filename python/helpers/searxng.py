import aiohttp
from python.helpers import runtime, dotenv

# 从环境变量获取 SearXNG URL，如果没有则使用默认值
URL = dotenv.get_dotenv_value("SEARXNG_URL") or "http://localhost:80/search"

async def search(query:str):
    return await runtime.call_development_function(_search, query=query)

async def _search(query:str):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data={"q": query, "format": "json"}) as response:
            return await response.json()
