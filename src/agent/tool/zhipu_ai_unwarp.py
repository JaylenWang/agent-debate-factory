import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import uuid

import aiohttp
import requests
from autogen._pydantic import PYDANTIC_V1
from pydantic import BaseModel, Extra, root_validator

ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/tools"

def get_from_dict_or_env(data: Dict[str, Any], key: str, env_key: str, default: Optional[str] = None) -> str:
    """Get a value from a dictionary or an environment variable."""
    if key in data and data[key]:
        return data[key]
    elif env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )
        
class ZhipuSearchAPIWrapper(BaseModel):
    zhipu_api_key: Optional[str] = None
    
    class Config:
        extra = Extra.forbid
    
    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        zhipu_api_key = get_from_dict_or_env(
            values, "zhipu_api_key", "ZHIPU_API_KEY"
        )
        values["zhipu_api_key"] = zhipu_api_key
        
        return values
    
    def raw_results(
        self,
        query: str,
        max_results: Optional[int] = 4,
        search_depth: Optional[str] = "advanced",
        include_domains: Optional[List[str]] = [],
        exclude_domains: Optional[List[str]] = [],
        include_answer: Optional[bool] = False,
        include_raw_content: Optional[bool] = False,
        include_images: Optional[bool] = False,
    ) -> Dict:
        msg = [
            {
                "role": "user",
                "content":query
            }
        ]
        tool = "web-search-pro"
        request_id = str(uuid.uuid4())
        params = {
            "request_id": request_id,
            "tool": tool,
            "stream": False,
            "messages": msg
        }
        # params = {
        #     "api_key": self.zhipu_api_key,
        #     "query": query,
        #     "max_results": max_results,
        #     "search_depth": search_depth,
        #     "include_domains": include_domains,
        #     "exclude_domains": exclude_domains,
        #     "include_answer": include_answer,
        #     "include_raw_content": include_raw_content,
        #     "include_images": include_images,
        # }
        resp = requests.post(
            ZHIPU_API_URL,
            json=params,
            headers={
                "Authorization": self.zhipu_api_key
            },
            timeout=300
        )
        resp.raise_for_status()
        response = resp.content.decode()
        response = json.loads(response)
        zhipu_results = response["choices"][0]['message']['tool_calls'][1]
        return zhipu_results
    
    def run(
        self,
        query: str,
        max_results: Optional[int] = 5,
        search_depth: Optional[str] = "advanced",
        include_domains: Optional[List[str]] = [],
        exclude_domains: Optional[List[str]] = [],
        include_answer: Optional[bool] = True,
        include_raw_content: Optional[bool] = False,
        include_images: Optional[bool] = False,
    ) -> List[Dict]:
        from urllib.error import HTTPError
        
        raw_search_results = None
        for _ in range(20):
            try:
                raw_search_results = self.raw_results(
                    query,
                    max_results,
                    search_depth,
                    include_domains,
                    exclude_domains,
                    include_answer,
                    include_raw_content,
                    include_images,
                )
                break
            except HTTPError:
                import time
                time.sleep(2)
            except Exception:
                return (
                    "Error. Zhipu wasn't able to answer it. Please try a new query for Zhipu or use other tools.",
                    False,
                )
        if raw_search_results["search_result"] is None:
            print(f"查询：{query} 时出现错误，跳过该关键词。")
            return (
                "Error. Zhipu wasn't able to answer it. Please try a new query for Zhipu or use other tools.",
                True,
            )
        # if include_answer:
        #     return self.format_result(raw_search_results["results"], answer=raw_search_results["answer"]), True
        return self.format_result(raw_search_results["search_result"]), True
    
    def format_result(self, results: List[Dict], answer = None) -> str:
        if answer is not None:
            format_result = answer
        else:
            format_result = ""
        
        for result in results:
            format_result += f"URL: {result['link']}\nContent: {result['content']}\n\n"
        return format_result
    
    def clean_results(self, results: List[Dict]) -> List[Dict]:
        clean_results = []
        for result in results:
            clean_results.append(
                {
                    "url": result["link"],
                    "content": result["content"]
                }
            )
        return clean_results