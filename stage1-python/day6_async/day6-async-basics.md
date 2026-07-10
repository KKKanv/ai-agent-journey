# Day 6: async/await 异步编程基础

> 第一阶段 Python 速通 — 第六天  
> 目标：理解事件循环机制，掌握 async/await 核心语法  
> 前置：Python 3.7+（推荐 3.10+）

---

## 1. 为什么要学异步？

### 同步的痛点

```python
import time

def fetch_url(url):
    print(f"开始请求: {url}")
    time.sleep(2)           # 模拟网络 IO（耗时操作）
    print(f"完成: {url}")
    return f"data from {url}"

# 依次请求 3 个 URL → 总共 6 秒
fetch_url("https://api1.com")
fetch_url("https://api2.com")
fetch_url("https://api3.com")
```

```
总耗时: 6 秒  ← 大部分时间在等 IO，CPU 空闲
```

### 异步的思路

> 等待 IO 时让 CPU 去干别的活，等数据回来了再回来处理。

```python
import asyncio

async def fetch_url(url):
    print(f"开始请求: {url}")
    await asyncio.sleep(2)       # 模拟异步 IO（不阻塞）
    print(f"完成: {url}")
    return f"data from {url}"

# 并发请求 3 个 URL → 总共 ~2 秒
async def main():
    tasks = [fetch_url("https://api1.com"),
             fetch_url("https://api2.com"),
             fetch_url("https://api3.com")]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

```
总耗时: ~2 秒  ← 并发等待，3 个请求同时进行
```

### 适用场景

| 场景 | 适合异步？ | 原因 |
|------|-----------|------|
| Web API 调用 | ✅ | IO 密集，天然并发 |
| 数据库查询 | ✅ | 等待数据库返回时不阻塞 |
| 文件读写 | ✅ | 用 aiofiles |
| Agent Tool 调用 | ✅ **必须用** | Agent 并发调用多个 Tool |
| CPU 密集计算 | ❌ | 异步不能加速 CPU 计算（用多进程） |
| 简单脚本 | ❌ 没必要 | 同步更简单 |

---

## 2. 核心概念

### 2.1 事件循环 (Event Loop)

```
┌─────────────────────────────────────────────┐
│                Event Loop                    │
│                                              │
│   ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │
│   │ T1  │  │ T2  │  │ T3  │  │ T4  │ ...   │
│   │等待IO│  │就绪 │  │等待IO│  │等待IO│       │
│   └─────┘  └─────┘  └─────┘  └─────┘       │
│       ↑        ↑                              │
│       │    CPU 执行这个                        │
│       └──── 数据回来了，回到队列              │
└─────────────────────────────────────────────┘
```

- **事件循环**是一个无限循环，负责调度和运行协程
- 当一个协程 `await` 时，它"让出"控制权，事件循环去跑别的协程
- 当被等待的操作完成，协程被重新调度继续执行

### 2.2 协程 (Coroutine)

协程就是 `async def` 定义的函数。调用它**不会立即执行**，而是返回一个协程对象。

```python
async def say_hello():
    return "Hello"

# 调用 → 返回协程对象
coro = say_hello()
print(type(coro))          # <class 'coroutine'>

# 协程需要被"驱动"才能执行
# 方式 1：asyncio.run()
result = asyncio.run(say_hello())
print(result)              # "Hello"

# 方式 2：在另一个 async 函数中 await
# (见下文)
```

### 2.3 await — 交出控制权

`await` 做了两件事：
1. **交出 CPU**：告诉事件循环"我要等，你先去跑别的"
2. **等结果**：当被 await 的对象完成，拿到返回值继续执行

```python
async def step1():
    print("步骤 1 开始")
    await asyncio.sleep(1)    # 等 1 秒，期间让出控制权
    print("步骤 1 结束")
    return "结果 A"

async def step2():
    print("步骤 2 开始")
    await asyncio.sleep(1)    # 等 1 秒，期间让出控制权
    print("步骤 2 结束")
    return "结果 B"

async def main():
    # 不并发——顺序执行（总共 2 秒）
    a = await step1()      # 等 step1 完全结束
    b = await step2()      # 再开始 step2
    print(a, b)

asyncio.run(main())
```

```
执行顺序：
步骤 1 开始
(等 1 秒)
步骤 1 结束
步骤 2 开始
(等 1 秒)
步骤 2 结束
结果 A 结果 B
```

### 2.4 可等待对象 (Awaitable)

`await` 后面可以跟三种东西：

| 类型 | 说明 | 常见用法 |
|------|------|----------|
| **协程** (Coroutine) | `async def` 函数返回值 | `await my_func()` |
| **任务** (Task) | 包装后的协程，可以并发 | `await asyncio.create_task(...)` |
| **Future** | 低层接口，一般不用 | `await loop.create_future()` |

> 💡 99% 的情况下你只需要用协程和 Task。

---

## 3. 核心 API 速查

### 3.1 asyncio.run()

**统一入口**：启动事件循环，运行一个协程，结束后清理。

```python
import asyncio

async def main():
    print("Hello async!")
    await asyncio.sleep(1)
    print("Done!")

asyncio.run(main())
# ↑ 这是唯一"暴露"给同步代码的接口
```

> ⚠️ 同一个线程中**不能**嵌套调用 `asyncio.run()`
> 一个 asyncio.run() 对应一个事件循环

### 3.2 asyncio.sleep()

异步版的 `time.sleep()` —— 不会阻塞线程。

```python
await asyncio.sleep(1)       # 等 1 秒
await asyncio.sleep(0)       # 让出控制权，立即重新调度
```

### 3.3 asyncio.gather()

**并发运行多个协程**，等待所有完成。

```python
async def fetch(url):
    await asyncio.sleep(1)
    return f"data from {url}"

async def main():
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )
    print(results)
    # ['data from url1', 'data from url2', 'data from url3']

asyncio.run(main())
```

**重要参数：**

| 参数 | 作用 |
|------|------|
| `return_exceptions=True` | 有异常时以异常对象返回，不中断其他任务 |
| `return_exceptions=False`（默认） | 任一协程异常，全部取消 |

```python
async def fail():
    raise ValueError("出错了")

async def main():
    results = await asyncio.gather(
        fetch("url1"),
        fail(),
        fetch("url2"),
        return_exceptions=True,    # 失败不影响其他任务
    )
    print(results)
    # ['data from url1', ValueError('出错了'), 'data from url2']

asyncio.run(main())
```

### 3.4 asyncio.create_task()

创建一个 Task，让协程**在后台运行**。

```python
async def main():
    # 创建任务 → 协程开始在后台运行
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))

    # 做点其他事...
    print("两个任务在后台跑着")

    # 等任务完成
    result1 = await task1
    result2 = await task2

    print(result1, result2)
```

**`gather` vs `create_task`：**

| | gather | create_task |
|------|--------|-------------|
| 同时启动多个 | ✅ 自动 | ✅ |
| 等所有完成 | ✅ 自动 await | 需手动 await |
| 返回结果 | ✅ 列表 | await 单个 |
| 单个处理异常 | ✅ `return_exceptions=True` | 需 try/except |
| 需要逐个 await | ❌ 不 | ✅ 可以穿插 |

```python
# create_task 的优势：可以不一启动就等
async def main():
    task = asyncio.create_task(slow_operation())
    print("先做点别的...")
    await asyncio.sleep(0.3)
    print("差不多了，等结果")
    result = await task       # 此时慢操作可能已经完成了
```

### 3.5 asyncio.wait()

更灵活的等待方式：

```python
# asyncio.wait 可以控制等待策略
done, pending = await asyncio.wait(
    [task1, task2, task3],
    timeout=2.0,              # 最多等 2 秒
    return_when="FIRST_COMPLETED",  # 第一个完成就返回
)

for task in done:
    print(task.result())
```

`return_when` 可选值：
- `ALL_COMPLETED`（默认）— 所有完成
- `FIRST_COMPLETED` — 第一个完成（如竞态请求）
- `FIRST_EXCEPTION` — 第一个异常或全部完成

---

## 4. 错误处理

### 4.1 try/await/except

```python
async def safe_fetch(url):
    try:
        data = await fetch(url)
        return data
    except aiohttp.ClientError as e:
        print(f"网络错误: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"超时: {url}")
        return None
```

### 4.2 gather 中的错误处理

```python
async def main():
    tasks = [
        fetch("url1"),
        fetch("url2"),
        failing_task(),
    ]

    # 方式 1：return_exceptions=True
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            print(f"有任务失败了: {r}")
        else:
            print(f"成功: {r}")

    # 方式 2：逐个包装 try/except
    results = await asyncio.gather(
        *(safe_fetch(url) for url in urls)
    )
```

---

## 5. asyncio 常用工具

| 函数 | 作用 |
|------|------|
| `asyncio.run(main())` | 入口：启动事件循环 |
| `asyncio.sleep(sec)` | 异步等待 |
| `asyncio.gather(*coros)` | 并发执行，等所有完成 |
| `asyncio.create_task(coro)` | 创建后台任务 |
| `asyncio.wait(tasks, **kw)` | 灵活等待 |
| `asyncio.as_completed(tasks)` | 按完成顺序迭代 |
| `asyncio.timeout(sec)` (3.11+) | 超时上下文管理器 |
| `asyncio.wait_for(coro, timeout)` | 带超时的 await |

### asyncio.as_completed — 谁先完成先处理谁

```python
async def main():
    tasks = [fetch(f"url{i}") for i in range(5)]

    for coro in asyncio.as_completed(tasks):
        result = await coro          # 谁先完成，谁先被处理
        print(f"拿到结果: {result}")
```

### asyncio.timeout — 超时控制 (Python 3.11+)

```python
async def main():
    try:
        async with asyncio.timeout(3):
            result = await slow_fetch()
    except asyncio.TimeoutError:
        print("请求超时！")
```

3.11 之前用 `asyncio.wait_for`：

```python
try:
    result = await asyncio.wait_for(fetch("url"), timeout=3)
except asyncio.TimeoutError:
    print("超时！")
```

---

## 6. 常见陷阱

### ❌ 陷阱 1：在 async 函数里用 time.sleep

```python
async def bad():
    time.sleep(1)       # 会阻塞整个事件循环！所有协程都卡住
```

✅ 正确：
```python
async def good():
    await asyncio.sleep(1)   # 让出控制权
```

### ❌ 陷阱 2：忘记 await

```python
async def main():
    result = fetch_url()      # ❌ 没 await → 返回 coroutine，不是结果！
    result = await fetch_url() # ✅
```

### ❌ 陷阱 3：在同步代码里调用 async 函数

```python
def sync_func():
    asyncio.run(async_func())   # ✅ 正确

    await async_func()          # ❌ await 只能在 async 函数里用
```

### ❌ 陷阱 4：创建 Task 后忘了管它

```python
async def main():
    asyncio.create_task(some_work())    # 任务可能没跑完就被回收了
    # ⚠️ 程序结束时未完成的 Task 会输出警告
```

✅ 正确：`await` 或存引用：
```python
async def main():
    task = asyncio.create_task(some_work())
    # ... 做其他事 ...
    await task    # 确保完成
```

---

## 总结

```
✅ 异步 = IO 等待时不阻塞，让 CPU 干别的
✅ async def 定义协程，await 交出控制权
✅ asyncio.run() 是入口
✅ asyncio.gather() 并发跑多个协程
✅ asyncio.create_task() 创建后台任务
✅ 异步 IO 密集场景，不能加速 CPU 计算
✅ 记住：time.sleep → asyncio.sleep，忘 await → 翻车
```
