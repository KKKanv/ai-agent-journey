"""
练习 2：模拟并发 API 请求

目标：用 asyncio.gather() 模拟并发获取多个数据源，处理返回结果。
"""

import asyncio
import random


# 模拟从不同数据源获取数据
async def fetch_from_source(name: str, delay: float):
    """
    模拟一个 API 请求。
    delay: 模拟网络延迟（秒）
    """
    await asyncio.sleep(delay)

    # 模拟返回数据
    data = {
        "source": name,
        "delay": delay,
        "value": random.randint(1, 100),
        "status": "ok",
    }
    return data


async def main():
    # 定义 5 个不同的数据源，延迟各不相同
    sources = [
        ("用户服务", 1.2),
        ("订单服务", 2.5),
        ("商品服务", 0.8),
        ("支付服务", 1.8),
        ("物流服务", 3.0),
    ]

    print("🚀 开始并发请求 5 个数据源...")
    print("-" * 40)

    start = asyncio.get_event_loop().time()

    # 并发请求所有数据源
    results = await asyncio.gather(
        *(fetch_from_source(name, delay) for name, delay in sources),
        return_exceptions=True,
    )

    elapsed = asyncio.get_event_loop().time() - start

    print(f"\n✅ 全部返回！总耗时: {elapsed:.2f} 秒")
    print("-" * 40)

    # 处理结果
    success_count = 0
    for result in results:
        if isinstance(result, Exception):
            print(f"❌ 请求失败: {result}")
        else:
            success_count += 1
            print(f"  [{result['source']}] value={result['value']}, "
                  f"delay={result['delay']}s")

    print(f"\n成功: {success_count}/{len(sources)}")

    # 计算汇总
    values = [r["value"] for r in results if not isinstance(r, Exception)]
    if values:
        print(f"\n📊 汇总:")
        print(f"  总值: {sum(values)}")
        print(f"  平均: {sum(values) / len(values):.1f}")
        print(f"  最大: {max(values)}")
        print(f"  最小: {min(values)}")


if __name__ == "__main__":
    asyncio.run(main())
