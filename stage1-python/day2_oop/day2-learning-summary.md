# Day 2 学习总结：Python 面向对象 + 异常处理 + 综合实战

> **日期：** 2026-06-19  
> **阶段：** 第一阶段（Python + FastAPI 速通）Day 2/10  
> **主题：** 函数、类、异常处理、文件 IO、魔术方法、综合实战  
> **前置背景：** 211 CS 大三，已学 C 语言  
> **源文件：** D:\Transform\ai-agent-journey\stage1-python\day2_oop\

---

## 一、学习位置

```
第一阶段时间线：
├── Day 1-2：Python 基础语法 ✅ 今天完成
├── Day 3：  推导式 + lambda + 装饰器
├── Day 4：  文件 IO + JSON/CSV
├── Day 5-6：async/await 异步编程
├── Day 7-8：FastAPI 写 API
└── Day 9-10：综合检验 + pytest
```

**今日目标：** 函数、类、异常处理融会贯通，能用类封装完整功能。

---

## 二、完成的 5 道练习题

### 🟢 题 1：灵活参数函数 — `describe_student`

**文件：** `test1.py`

**核心知识点：**

| 知识点 | 解释 |
|--------|------|
| `**kwargs` | 接收任意关键字参数，本质是一个 `dict`，调用方写 `score=92` → 函数内收到 `{'score': 92}` |
| `f-string` | `f"{变量}"` 是 Python 3.6+ 最推荐的字符串格式化，`{}` 内可以放变量或表达式 |
| `dict.items()` | 返回键值对元组，配合 `for key, value in ...` 拆包同时拿到键和值 |
| 列表推导式 | `[表达式 for 变量 in 可迭代对象]` — 把声明容器 + 循环 + 生成元素 + 插入容器四步合并为一行 |
| `", ".join(list)` | 用分隔符连接列表，底层 C 实现 O(n)，替代 C++ 循环 `+=` 的 O(n²) |

**列表 vs 生成器：**

| 写法 | 类型 | 执行时机 | 内存 |
|------|------|----------|------|
| `[...]` 列表推导式 | `list` | 立即执行，一次性生成全部 | 较大 |
| `(...)` 生成器表达式 | `generator` | 惰性求值，用到才生成 | 较小 |
| 去掉括号直接写 | ❌ `SyntaxError` | — | — |

> 当生成器表达式作为函数唯一参数时，外层括号可省略，如 `", ".join(f"{k}: {v}" for k, v in d.items())`

---

### 🟢 题 2：类封装 — `WordCounter`

**文件：** `test2.py`

**核心知识点：**

**① 正则提取单词：**
```python
import re
self.words = re.findall(r'\b\w+\b', text.lower())
```
- `\b` = 单词边界（空格、标点、字符串开头/结尾）
- `\w+` = 一个或多个字母/数字/下划线
- 一步到位：小写 + 去标点 + 拆分，无需预处理

**② 三种文本处理方案对比：**

| 方案 | 代码 | 性能 | 缺陷 |
|------|------|------|------|
| 循环 `replace` | `for ch in string.punctuation: text.replace(ch, ' ')` | O(n×32)，复制 32 次 | "don't" 被拆开 |
| `re.findall` | `re.findall(r'\b\w+\b', text)` | C 层高效 | `\w` 匹配下划线 |
| `str.translate` | `text.translate(table).split()` | 极快，纯 C | 需建映射表 |

**③ 字典计数标准写法：**
```python
self.freq[word] = self.freq.get(word, 0) + 1
```
- `dict.get(key, default)`：键存在返回值，不存在返回 `default`
- 效果：存在则累加，不存在则初始化为 1
- 等价于 `collections.Counter` 的手动版本

**④ 稳定排序取 Top-N：**
```python
sorted(self.freq.items(), key=lambda x: x[1], reverse=True)[:n]
```
- `key=lambda x: x[1]` 按值（次数）排序
- `reverse=True` 降序
- Python 的 `sorted` 是稳定排序，相同次数保持字典插入顺序

> ⚠️ 题目示例 `count() # 8` 是笔误，实际文本有 9 个单词，以实际逻辑为准。

---

### 🟡 题 3：异常处理 — `safe_load_json`

**文件：** `test3.py`

**核心知识点：**

```python
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
except FileNotFoundError:
    print(f"[WARNING] File not found: {filepath}")
    return {}
except json.JSONDecodeError as e:
    print(f"[WARNING] Invalid JSON: {e}")
    return {}
```

| 要点 | 说明 |
|------|------|
| `with` 上下文管理器 | 自动关闭文件，即使发生异常也会释放资源 |
| 多分支 `except` | 精准捕获不同异常，比裸 `except Exception` 更规范 |
| `as e` | 把异常对象绑定到变量 `e`，可访问错误详情 |
| 统一返回 `{}` | 出错返回空字典而非 `None`，调用方更安全 |

---

### 🟡 题 4：魔术方法 — `Student` 类

**文件：** `test4.py`

**核心知识点：**

**① 魔术方法速查表：**

| 魔术方法 | 英文全称 | 触发时机 |
|----------|----------|----------|
| `__init__` | Initialize | `obj = Class()` |
| `__str__` | String | `print(obj)` / `str(obj)` |
| `__repr__` | Representation | REPL 输入变量名 / `repr(obj)` |
| `__lt__` | Less Than | `<` 运算符 |
| `__gt__` | Greater Than | `>` 运算符 |
| `__eq__` | Equal | `==` 运算符 |

**② `__str__` vs `__repr__` 回退逻辑：**
- `print(obj)` → 优先 `__str__`，没有则回退 `__repr__`
- REPL 输入 `obj` → 只调 `__repr__`，**绝不**回退 `__str__`
- `__repr__` 是兜底方案，`__str__` 是用户友好覆盖

**③ 比较运算符回退机制：**
- `s1 > s2` → 先找 `s1.__gt__(s2)` → 找不到 → 交换操作数 `s2.__lt__(s1)`
- 只需定义 `__lt__` + `__eq__`，Python 自动推导 `>` `<=` `>=` `!=`

**④ `isinstance` + `NotImplemented` 规范：**
```python
def __lt__(self, other):
    if not isinstance(other, Student):
        return NotImplemented  # 礼貌拒绝，让 Python 尝试反向比较
    return self.score < other.score
```
- `NotImplemented` ≠ 报错，是让 Python 换对方试试
- 双方都不知道怎么比，才抛 `TypeError`

**⑤ 魔术方法本质：**
- 双下划线 `__xxx__` 是 Python 内部保留命名，称为 Dunder Method
- 不是让你手动调用的，而是当使用内置函数或运算符时，**解释器自动调用的钩子**
- 类比：电器的插孔 — 你按遥控器，解释器自动去读插孔

---

### 🔴 题 5：综合实战 — `APIClient` 模拟器

**文件：** `test5.py`

**核心知识点：**

**① 自定义异常：**
```python
class InvalidAPIKeyError(ValueError):    # 继承 ValueError
    pass
class MaxRetryError(RuntimeError):       # 继承 RuntimeError
    pass
```

**② 重试循环模式（Agent 开发核心模式）：**
```
while 未超过重试次数:
    try:
        执行请求 → 成功则 return
    except 临时错误 as e:
        if 还有重试机会:
            print + time.sleep(1) → 等待后继续循环
        else:
            raise MaxRetryError(...) from e  # 包装后抛出
```

**③ `raise ... from e` — 异常链：**
- 保留原始异常上下文（`__cause__`）
- 上层看到：`MaxRetryError` 原因 → `ConnectionError: 网络超时`
- 不丢失根本原因的前提下，包装为业务可理解的异常

**④ `time.sleep(1)`：**
- 阻塞当前线程 1 秒，让出 CPU
- 防止瞬时高频重试打爆目标服务

**⑤ 局部变量 vs 实例属性：**
```python
# ❌ 副作用：改了 self.max_retries，__repr__ 跟着变
def chat(self, messages, max_retries=3):
    self.max_retries = max_retries

# ✅ 使用局部变量
def chat(self, messages, max_retries=3):
    retries = max_retries
```

---

## 三、Python vs C++ 知识迁移对照表

| 概念 | C++ | Python |
|------|-----|--------|
| 构造函数 | `ClassName() { }` | `__init__(self)` — 仅初始化，不分配内存 |
| 字符串格式化 | `printf` / `ostringstream` | `f"{var}"` — 更简洁直观 |
| 异常处理 | `try { } catch(T& e) { }` | `try: except T as e:` — 无类型声明 |
| 遍历映射 | `for (auto& p : m)` → `p.first/p.second` | `for k, v in d.items()` — 元组拆包 |
| 列表构建 | `vector + push_back` 循环 | `[expr for x in seq]` — 列表推导式合一 |
| 字符串拼接 | `+=` 循环 (O(n²)) | `",".join(list)` (O(n), C 层实现) |
| 运算符重载 | `operator<(const T&)` | `__lt__(self, other)` — 魔术方法 |
| 异常重新抛出 | `throw;` | `raise ... from e` — 异常链保留原因 |

---

## 四、今日核心收获

1. **`**kwargs`** + **列表推导式** + **f-string**：Python 三合一简洁表达力
2. **正则 `re.findall(r'\b\w+\b')`**：文本提取最佳方案
3. **`dict.get(key, 0) + 1`**：计数器标准写法
4. **魔术方法体系**：`__init__` `__str__` `__repr__` `__lt__` `__eq__` 的含义与触发时机
5. **比较运算符回退机制**：只定义 `__lt__` + `__eq__` → 全部比较运算符可用
6. **`isinstance` + `NotImplemented`**：安全比较的规范写法
7. **异常处理全套**：`try/except/as/raise...from` — Agent 重试逻辑的基石
8. **`join` vs C++ `+=`**：底层 O(n) vs O(n²) 的效率差异
9. **`time.sleep`** + **重试循环** + **异常链**：API 调用的核心模式

---

## 五、明日预告（Day 3）

**内容：** 列表/字典/集合推导式 + `lambda` + 装饰器  
**重点：** Python 独有的"语法糖日"，C 里完全没有的东西，需要新建立认知  
**前置需求：** 今天的函数和类已熟练掌握

---

## 六、对应路线图原文

```
第一阶段 Day 1-2：
├── 基础语法：类型、分支、循环、函数、类（2天）
│   └── ✅ 已完成 — 通过 5 道题从函数到综合实战
├── 列表/字典/集合推导式 + lambda + 装饰器（1天）→ ⏭️ Day 3
├── 文件 IO + json/csv 处理（1天）
├── 虚拟环境 venv/conda + pip（半天）
├── async/await 异步编程（2天）
├── FastAPI 写简单 API（2天）
└── pytest 写测试（半天）

第一阶段终极目标：用 FastAPI 写一个带异步调用的接口，接收问题返回答案
```
