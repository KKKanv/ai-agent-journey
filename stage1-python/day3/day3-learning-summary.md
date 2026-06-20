# Day 3 学习总结：推导式 + lambda + 装饰器

> **日期：** 2026-06-20  
> **阶段：** 第一阶段（Python + FastAPI 速通）  
> **主题：** 列表/字典/集合推导式、lambda 匿名函数、装饰器

---

## 一、练习一：推导式（Comprehensions）

**文件：** `practice1.py`

### 掌握内容

| 推导式类型         | 语法                                               | 示例                                                         |
| ------------------ | -------------------------------------------------- | ------------------------------------------------------------ |
| 列表推导式         | `[expr for x in iterable if cond]`                 | `[u["name"] for u in users if u["age"] >= 18]`               |
| 字典推导式         | `{key: val for x in iterable if cond}`             | `{u["name"]: u["score"] for u in users if u["score"] >= 85}` |
| 集合推导式         | `{expr for x in iterable}`                         | `{u["age"] for u in users}`                                  |
| 嵌套推导式（拍平） | `[item for sublist in nested for item in sublist]` | `[num for row in [[1,2],[3,4]] for num in row]`              |

### 关键理解

- **嵌套推导式的执行顺序是「先外层、后内层」**，和普通 for 循环一致：
  ```python
  # 推导式
  [num for sublist in nested for num in sublist]
  
  # 等价于
  result = []
  for sublist in nested:      # 先外层
      for num in sublist:     # 再内层
          result.append(num)
  ```
- 推导式中的变量名（如 `user`、`a`）只是临时变量，可以自由命名

---

## 二、练习二：lambda 匿名函数

**文件：** `practice2.py`

### 掌握内容

| 高阶函数                   | 作用                     | 示例                                              |
| -------------------------- | ------------------------ | ------------------------------------------------- |
| `sorted(iter, key=lambda)` | 自定义排序               | `sorted(words, key=lambda w: len(w))`             |
| `sorted(... reverse=True)` | 降序排序                 | `sorted(pairs, key=lambda p: p[1], reverse=True)` |
| `filter(func, iter)`       | 筛选（返回 True 的保留） | `filter(lambda w: len(w) >= 5, words)`            |
| `map(func, iter)`          | 映射/转换每个元素        | `map(lambda p: f"{p[0]}:{p[1]}", pairs)`          |

### 关键理解

- **`sorted` 是"老板"，主动把每个元素喂给 lambda**——不是 lambda 自己知道 w 是谁
- `filter` 和 `map` 返回**迭代器**，需要用 `list()` 转换才能看到内容
- `filter` + `map` 与列表推导式的等价关系：
  ```python
  list(filter(lambda w: len(w)>=5, words))
  # 等价于
  [w for w in words if len(w) >= 5]
  
  list(map(lambda p: f"{p[0]}:{p[1]}", pairs))
  # 等价于
  [f"{p[0]}:{p[1]}" for p in pairs]
  ```
- `map` 的参数顺序：**函数在前，数据在后**——`map(func, iterable)`，这与 `sorted(iterable, key=func)` 不同
- 多可迭代对象时，`map` 以**最短的为准**，多余的被丢弃

---

## 三、练习三：装饰器（Decorator）

### 3.1 `@timer` — 计时装饰器

**文件：** `practice3.1 .py`

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.3f}s")
        return result
    return wrapper
```

**要点：**
- `@wraps(func)` 保留原函数的 `__name__`、`__doc__` 等元信息
- `time.perf_counter()` 高精度计时（比 `time.time()` 更适合性能测量）
- `@timer` 等价于 `slow_add = timer(slow_add)`

---

### 3.2 `@logger` — 日志装饰器

**文件：** `practice3.2 .py`

```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = ', '.join(repr(a) for a in args)
        kwargs_repr = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = args_repr
        if kwargs_repr:
            all_args += ', ' + kwargs_repr if args_repr else kwargs_repr

        print(f"[LOG] Calling {func.__name__} with args=({all_args})", end='')
        try:
            result = func(*args, **kwargs)
            print(f" -> returned {result!r}")
            return result
        except Exception as e:
            print(f" -> raised {type(e).__name__}: {e}")
            raise  # 重新抛出，不吞异常
    return wrapper
```

**要点：**
- `repr()` 让日志参数**类型明确无歧义**（字符串带引号、换行符显示为 `\n`）
- `!r` 在 f-string 中等价于 `repr()`
- `end=''` 让日志前半段不换行，返回值/异常接在同一行
- `raise` 必须保留——否则异常被**吞掉**，调用者收到 `None`，bug 极难排查

---

### 3.3 `@retry` — 重试装饰器（进阶）

**文件：** `practice3.3.py`

```python
import random
from functools import wraps

def retry(max_attempts=3):           # 装饰器工厂（带参数）
    def decorator(func):              # 真正的装饰器
        @wraps(func)
        def wrapper(*args, **kwargs): # 包装函数
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)  # 成功则立即返回
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        break
            raise last_exception       # 全部失败才抛异常
        return wrapper
    return decorator
```

**要点：**
- 这是一个**带参数的装饰器**（三层嵌套）：`retry()` → `decorator()` → `wrapper()`
- `return func(...)` 的三重作用：**① 调用原函数 ② 传递返回值 ③ 终止重试循环**
- 如果只写 `func(...)` 而不 `return`，返回值会被丢弃，`wrapper` 隐式返回 `None`
- **执行结构**：外层 5 次 × 内层最多 3 次，但成功即停，不是固定的 15 次

---

## 四、深度问答：今日踩坑与知识点

### 4.1 `*args` vs `**kwargs`

| 概念       | 接收             | 打包成       | 示例                           |
| ---------- | ---------------- | ------------ | ------------------------------ |
| `*args`    | 多余的位置参数   | 元组 `tuple` | `(1, 2, 3)`                    |
| `**kwargs` | 多余的关键字参数 | 字典 `dict`  | `{"name": "Alice", "age": 25}` |

- 位置参数：按顺序传入，`func(1, 2, 3)`
- 关键字参数：按名字传入，`func(a=1, c=3, b=2)`（顺序无关）
- 位置参数必须在关键字参数之前

### 4.2 `repr()` vs `str()` vs `!r`

| 对象             | `str()`              | `repr()`         |
| ---------------- | -------------------- | ---------------- |
| `"hello"`        | `hello`              | `'hello'`        |
| `"Hello\nWorld"` | `Hello` 换行 `World` | `'Hello\nWorld'` |
| `123`            | `123`                | `123`            |

- `repr()` 的目标：**适合开发者阅读的、无歧义的表示**
- `!r` 是 f-string 中的转换标志，等价于 `repr()`：`f"{v!r}"` = `f"{repr(v)}"`
- `fr"..."` 可以组合使用：f（插值） + r（不转义反斜杠），但 `r` 只作用于字面量，不影响已存储的变量

### 4.3 `try/except/raise` 机制

- `except` 在 try 块**发生异常时立即跳转**，不会等 try 执行完
- **有 `raise`**：异常继续向上传播，调用者可以捕获处理
- **无 `raise`**：异常被吞掉，函数返回 `None`，bug 极难排查
- **捕获的异常不会让函数停止**——函数继续执行 except 块及之后的代码
- **未被捕获的异常会立即终止函数**——剩余代码全部跳过

### 4.4 条件表达式优先级

```python
all_args += ', ' + kwargs_repr if args_repr else kwargs_repr
# 等价于
all_args += (', ' + kwargs_repr if args_repr else kwargs_repr)
```
三元表达式先于 `+=` 求值，再加括号等于 `if-else` 清晰写法。

### 4.5 其他实用技巧

- `end=''` 控制 `print` 不换行，让后续输出接在同一行
- 装饰器中 `return` 既是传值也是**终止循环**的控制流
- 文件名避免空格，命令行中容易引起歧义

---

## 五、今日掌握情况

| 知识点                      | 状态 | 关键产出               |
| --------------------------- | ---- | ---------------------- |
| 列表/字典/集合推导式        | ✅    | 4 道练习题             |
| 嵌套推导式（拍平）          | ✅    | 理解执行顺序           |
| `sorted` + `lambda`         | ✅    | 5 种排序/过滤/映射     |
| `filter` / `map` + `lambda` | ✅    | 理解与推导式的等价关系 |
| `@timer` 基础装饰器         | ✅    | 闭包 + `@wraps`        |
| `@logger` 日志装饰器        | ✅    | `repr()` + 异常处理    |
| `@retry` 带参数装饰器       | ✅    | 三层嵌套 + 重试逻辑    |
| `*args` / `**kwargs`        | ✅    | 位置 vs 关键字参数     |
| `repr()` / `!r` / `fr"..."` | ✅    | 字符串格式化深入       |
| `try/except/raise` 流程     | ✅    | 异常传播机制           |

---

> **下一天：** 第一阶段 Day 4 — 文件 IO + JSON/CSV 处理
