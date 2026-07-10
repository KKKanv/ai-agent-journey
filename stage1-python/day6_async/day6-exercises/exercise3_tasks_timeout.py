"""
练习 3：后台任务 + 超时控制

目标：用 create_task 在后台运行耗时操作，同时做别的事；
      用 asyncio.timeout 控制超时。
"""

import asyncio


async def slow_operation(name: str, duration: float):
    """模拟一个耗时操作"""
    print(f"  ⏳ [{name}] 开始，需要 {duration} 秒...")
    await asyncio.sleep(duration)
    print(f"  ✅ [{name}] 完成！")
    return f"{name} 的结果"


async def main():
    print("=== 场景 1: 先做别的事，等后台任务 ===")
    print()

    # 启动一个耗时 3 秒的后台任务
    task = asyncio.create_task(slow_operation("后台任务", 3))

    # 做点别的事
    print("📋 主流程：检查配置...")
    await asyncio.sleep(0.5)
    print("📋 主流程：加载缓存...")
    await asyncio.sleep(0.5)
    print("📋 主流程：验证用户...")
    await asyncio.sleep(0.5)

    # 等后台任务完成
    print("📋 主流程：等后台任务结果...")
    result = await task
    print(f"📋 拿到结果: {result}")
    print()

    # ========================

    print("=== 场景 2: 超时控制 ===")
    print()

    # 定义三个延迟不同的任务
    tasks_config = [
        ("快速查询", 1),
        ("中等查询", 3),
        ("慢速查询", 6),
    ]

    async def fetch_with_timeout(name: str, delay: float, timeout: float):
        try:
            # Python 3.11+ 写法
            try:
                async with asyncio.timeout(timeout):
                    result = await slow_operation(name, delay)
                    return (name, result)
            except asyncio.TimeoutError:
                print(f"  ⛔ [{name}] 超时！（超过 {timeout} 秒）")
                return (name, None)
        except AttributeError:
            # Python 3.10 及以下用 wait_for
            try:
                result = await asyncio.wait_for(
                    slow_operation(name, delay),
                    timeout=timeout,
                )
                return (name, result)
            except asyncio.TimeoutError:
                print(f"  ⛔ [{name}] 超时！（超过 {timeout} 秒）")
                return (name, None)

    # 统一设 4 秒超时
    timeout = 4.0
    print(f"⏰ 统一超时: {timeout} 秒")
    results = await asyncio.gather(*(
        fetch_with_timeout(name, delay, timeout)
        for name, delay in tasks_config
    ))

    print()
    print("📊 最终结果:")
    for name, result in results:
        if result:
            print(f"  ✅ {name}: {result}")
        else:
            print(f"  ❌ {name}: 超时/失败")
    print()

    # ========================

    print("=== 场景 3: 竞态请求（谁先返回用谁的）===")
    print("向两个服务发出相同请求，用第一个返回的结果")

    async def race():
        task_a = asyncio.create_task(slow_operation("服务 A（快）", 1.0))
        task_b = asyncio.create_task(slow_operation("服务 B（慢）", 3.0))

        # 谁先完成返回谁
        done, pending = await asyncio.wait(
            [task_a, task_b],
            return_when="FIRST_COMPLETED",
        )

        # 取消还在跑的
        for task in pending:
            task.cancel()
            print(f"  🗑️ 取消未完成的任务")

        # 拿到第一个结果
        winner = done.pop()
        print(f"  🏆 胜出: {winner.result()}")

    await race()


if __name__ == "__main__":
    asyncio.run(main())
