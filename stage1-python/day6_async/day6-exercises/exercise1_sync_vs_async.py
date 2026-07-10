"""
练习 1：理解协程 vs 普通函数

目标：感受 async/await 的基本执行流程，对比同步和异步的时间差。
"""

import asyncio
import time

# ===== 同步版本 =====
def sync_count(name: str, n: int):
    for i in range(1, n + 1):
        time.sleep(0.5)
        print(f"  [{name}] 第 {i} 步")
    return f"{name} 完成"

def run_sync():
    print("=== 同步版本（顺序执行）===")
    start = time.time()
    sync_count("A", 3)
    sync_count("B", 3)
    end = time.time()
    print(f"同步耗时: {end - start:.2f} 秒\n")

# ===== 异步版本 =====
async def async_count(name: str, n: int):
    for i in range(1, n + 1):
        await asyncio.sleep(0.5)
        print(f"  [{name}] 第 {i} 步")
    return f"{name} 完成"

async def run_async():
    print("=== 异步版本（并发执行）===")
    start = time.time()
    # 并发执行 A 和 B
    await asyncio.gather(
        async_count("A", 3),
        async_count("B", 3),
    )
    end = time.time()
    print(f"异步耗时: {end - start:.2f} 秒\n")


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())

    print("-- 思考题 --")
    print("为什么同步要 3 秒，异步只要 1.5 秒？")
    print("如果两个函数一个跑 3 步一个跑 6 步，异步要多久？")
