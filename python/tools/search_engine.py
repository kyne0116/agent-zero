import os
import asyncio
from python.helpers import dotenv, memory, perplexity_search, duckduckgo_search
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from python.helpers.errors import handle_error
from python.helpers.searxng import search as searxng

SEARCH_ENGINE_RESULTS = 10


class SearchEngine(Tool):
    async def execute(self, query="", **kwargs):
        # 首先尝试 SearXNG
        try:
            searxng_result = await self.searxng_search(query)
            # 检查结果是否有效（不是错误信息且不为空）
            if (not searxng_result.startswith("Search Engine search failed") and
                searxng_result.strip() and
                len(searxng_result.strip()) > 10):  # 确保有实际内容
                await self.agent.handle_intervention(searxng_result)
                return Response(message=searxng_result, break_loop=False)
            else:
                PrintStyle(font_color="#FFA500").print(f"{self.agent.agent_name}: SearXNG returned empty or invalid results")
        except Exception as e:
            PrintStyle(font_color="red").print(f"{self.agent.agent_name}: SearXNG failed: {e}")

        # 如果 SearXNG 失败或返回空结果，回退到 DuckDuckGo
        PrintStyle(font_color="#0000FF").print(f"{self.agent.agent_name}: Falling back to DuckDuckGo search...")
        try:
            ddg_result = await self.duckduckgo_search(query)
            if ddg_result.strip() and len(ddg_result.strip()) > 10:
                await self.agent.handle_intervention(ddg_result)
                return Response(message=ddg_result, break_loop=False)
            else:
                error_msg = f"Both SearXNG and DuckDuckGo returned empty results for query: {query}"
                await self.agent.handle_intervention(error_msg)
                return Response(message=error_msg, break_loop=False)
        except Exception as e:
            error_msg = f"All search engines failed. SearXNG and DuckDuckGo are unavailable: {e}"
            await self.agent.handle_intervention(error_msg)
            return Response(message=error_msg, break_loop=False)


    async def searxng_search(self, question):
        results = await searxng(question)
        return self.format_result_searxng(results, "Search Engine")

    async def duckduckgo_search(self, question):
        results = duckduckgo_search.search(question)
        return self.format_result_duckduckgo(results, "DuckDuckGo")

    def format_result_searxng(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"

        outputs = []
        for item in result["results"]:
            outputs.append(f"{item['title']}\n{item['url']}\n{item['content']}")

        return "\n\n".join(outputs[:SEARCH_ENGINE_RESULTS]).strip()

    def format_result_duckduckgo(self, result, source):
        if isinstance(result, Exception):
            handle_error(result)
            return f"{source} search failed: {str(result)}"

        outputs = []
        for item_str in result:
            # DuckDuckGo 返回的是字符串列表，需要解析
            try:
                # 简单解析字符串格式的结果
                if "title" in item_str and "href" in item_str:
                    outputs.append(item_str)
            except:
                outputs.append(item_str)

        return "\n\n".join(outputs[:SEARCH_ENGINE_RESULTS]).strip()
