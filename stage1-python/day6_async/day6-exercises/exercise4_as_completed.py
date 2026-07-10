"""
练习 4：as_completed — 谁先完成先处理谁

目标：用 as_completed 按完成顺序处理结果，适合"有结果就展示"的场景。
"""

import asyncio
import random


async def fetch_user(user_id: int) -> dict:
    """模拟获取用户信息，延迟随机"""
    delay = round(random.uniform(0.5, 3.0), 1)
    await asyncio.sleep(delay)
    return {
        "user_id": user_id,
        "name": f"User_{user_id}",
        "delay": delay,
        "avatar": f"https://avatar.example.com/{user_id}.png",
    }


async def main():
    user_ids = [1, 2, 3, 4, 5, 6, 7, 8]

    print("🚀 并发获取用户信息...")
    print("（按完成顺序展示，不受请求顺序影响）")
    print("-" * 50)

    # 创建所有任务
    tasks = [fetch_user(uid) for uid in user_ids]

    start = asyncio.get_event_loop().time()
    count = 0

    # as_completed：按完成顺序迭代
    for coro in asyncio.as_completed(tasks):
        user = await coro
        count += 1
        elapsed = asyncio.get_event_loop().time() - start
        print(f"  [{elapsed:4.1f}s] #{count}  User_{user['user_id']:2d}  "
              f"（延迟 {user['delay']}s）")

    total = asyncio.get_event_loop().time() - start
    print("-" * 50)
    print(f"✅ 全部完成！总耗时: {total:.1f} 秒")
    print(f"   （如果同步做，需要 {sum(random.uniform(0.5, 3.0) for _ in range(8)):.1f} 秒）")


if __name__ == "__main__":
    asyncio.run(main())
