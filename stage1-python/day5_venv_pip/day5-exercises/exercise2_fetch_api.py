"""
练习 2：用虚拟环境中的包写一个 API 请求脚本

目标：在刚创建的 venv 中运行，调用一个公开 API 获取数据。

前置条件：
    - 已激活 venv（source venv/Scripts/activate）
    - 已安装 requests（pip install requests）

步骤：
    1. 确保 venv 已激活（提示符前有 (venv)）
    2. 运行这个脚本
    3. 观察输出

运行方式：
    (venv) $ python day5-exercises/exercise2_fetch_api.py
"""

import requests
import sys

print(f"正在使用的 Python: {sys.executable}")
print(f"Python 版本: {sys.version}")
print()

# 公开 API：获取一篇随机文章
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # 检查 HTTP 错误

    data = response.json()
    print("✅ 请求成功！")
    print(f"状态码: {response.status_code}")
    print()
    print(f"标题: {data['title']}")
    print(f"内容: {data['body']}")
    print()
    print(f"完整返回数据结构:")
    for key, value in data.items():
        print(f"  {key}: {value}")

except requests.exceptions.RequestException as e:
    print(f"❌ 请求失败: {e}")
