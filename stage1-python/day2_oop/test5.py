import random
import time
from typing import List, Dict, Any

# ---------- 自定义异常 ----------
class InvalidAPIKeyError(ValueError):
    """API Key 为空时抛出"""
    pass

class MaxRetryError(RuntimeError):
    """超过最大重试次数时抛出"""
    pass

# ---------- APIClient 类 ----------
class APIClient:
    def __init__(self, api_key: str, base_url: str):
        if not api_key or not api_key.strip():
            raise InvalidAPIKeyError("API Key cannot be empty")
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = 3  

    def chat(self, messages: List[Dict[str, str]], max_retries: int = 3) -> Dict[str, Any]:
        """
        模拟 AI API 调用，带重试机制。
        返回成功响应字典：{"role": "assistant", "content": "..."}
        """
        self.max_retries = max_retries   
        attempt = 0
        while attempt < max_retries:
            attempt += 1
            print(f"[LOG] 第 {attempt} 次尝试...")
            try:
                if random.random() < 0.7:   # 成功
                    return {
                        "role": "assistant",
                        "content": f"这是对 '{messages[-1]['content']}' 的模拟回复"
                    }
                else:
                    raise ConnectionError("模拟网络错误：请求超时")
            except ConnectionError as e:
                if attempt < max_retries:
                    print(f"   请求失败：{e}，1秒后重试...")
                    time.sleep(1)
                else:
                    raise MaxRetryError(f"重试 {max_retries} 次后仍然失败：{e}") from e
        raise MaxRetryError("未知错误：重试次数已耗尽")

    def __repr__(self) -> str:
        return f"APIClient(base_url={self.base_url}, retries_left={self.max_retries})"

# ---------- 测试 ----------
if __name__ == "__main__":
    client = APIClient(api_key="sk-xxx", base_url="https://api.anthropic.com")
    print(client)  # APIClient(base_url=https://api.anthropic.com, retries_left=3)

    try:
        resp = client.chat([{"role": "user", "content": "你在干什么"}])
        print(resp)
    except MaxRetryError as e:
        print(f"调用失败: {e}")

    try:
        bad_client = APIClient(api_key="", base_url="...")
    except InvalidAPIKeyError as e:
        print(f"初始化失败: {e}")