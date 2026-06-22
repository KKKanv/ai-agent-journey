# Day 4：文件 IO + JSON/CSV 处理

> 今日目标：熟练掌握 Python 文件读写 + JSON/CSV 序列化，能独立写脚本处理数据文件。

---

## 一、文件读写基础

### 1.1 核心：`open()` + `with`

```python
# ❌ 老式写法（容易忘 close）
f = open("data.txt", "r")
content = f.read()
f.close()

# ✅ 推荐：with 上下文管理器，自动关闭
with open("data.txt", "r") as f:
    content = f.read()
```

### 1.2 读文件的三种方式

```python
# 1. 一次性读全部（适合小文件）
with open("data.txt", "r") as f:
    content = f.read()          # 返回 str

# 2. 逐行读（适合大文件，省内存）
with open("data.txt", "r") as f:
    for line in f:              # line 会带末尾换行符 \n
        print(line.strip())     # strip() 去掉首尾空白/换行

# 3. readlines() → 列表（还行，但大文件不如逐行）
with open("data.txt", "r") as f:
    lines = f.readlines()       # 返回 list[str]
```

### 1.3 写文件

```python
lines = ["第一行\n", "第二行\n", "第三行\n"]

with open("output.txt", "w") as f:
    f.write("hello world\n")     # 写一个字符串
    f.writelines(lines)          # 写一个字符串列表
```

### 1.4 打开模式速查

| 模式 | 含义 | 文件不存在 |
|------|------|-----------|
| `"r"` | 只读 | 报错 |
| `"w"` | 只写（清空再写） | 新建 |
| `"a"` | 追加写 | 新建 |
| `"x"` | 新建再写 | 报错 |
| `"r+"` | 读写，不截断 | 报错 |
| `"b"` | 二进制模式，如 `"rb"` `"wb"` | — |

```python
# 追加模式 —— 常用场景：日志
with open("app.log", "a") as f:
    f.write(f"[INFO] 2026-06-21 10:00:00 任务完成\n")

# 二进制模式 —— 图片、音频等
with open("image.png", "rb") as f:
    raw_bytes = f.read()
```

### 1.5 编码处理（重要！）

```python
# ❌ Windows 默认 GBK，读写 UTF-8 文件会乱码
# ✅ 始终显式指定 encoding="utf-8"
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 写中文
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("你好世界")
```

> **坑点：** Windows 下 `open()` 默认编码是 `gbk`，而大部分数据文件是 `utf-8`。**永远写 `encoding="utf-8"`。**

---

## 二、os 模块与 pathlib

### 2.1 os（传统、够用）

```python
import os

# 路径
os.path.exists("data.txt")        # True/False
os.path.isfile("data.txt")        # 是文件？
os.path.isdir("mydir")            # 是目录？
os.path.getsize("data.txt")       # 文件大小（字节）

# 拼接（别用手动拼 `/` 或 `\\`）
path = os.path.join("data", "2026", "output.json")  # data/2026/output.json

# 拆分
dir_part = os.path.dirname("a/b/c.txt")   # "a/b"
file_part = os.path.basename("a/b/c.txt") # "c.txt"
name, ext = os.path.splitext("c.txt")     # ("c", ".txt")

# 遍历目录
for filename in os.listdir("mydir"):           # 只给名字，不含路径
    full = os.path.join("mydir", filename)

# 递归遍历（包括子目录）
for root, dirs, files in os.walk("mydir"):
    for f in files:
        full_path = os.path.join(root, f)

# 创建 / 删除
os.makedirs("a/b/c", exist_ok=True)    # 递归创建，exist_ok=True 不怕已存在
os.remove("old.txt")                    # 删文件
```

### 2.2 pathlib（现代、推荐）

```python
from pathlib import Path

# 路径对象
p = Path("data") / "2026" / "output.json"   # 用 / 拼接，太舒服了
print(p)   # data/2026/output.json

# 常用方法
p.exists()
p.is_file()
p.is_dir()
p.stat().st_size           # 文件大小
p.name                     # "output.json"
p.stem                     # "output"（无后缀）
p.suffix                   # ".json"
p.parent                   # Path("data/2026")
p.read_text(encoding="utf-8")    # 读文本
p.write_text("hello", encoding="utf-8")  # 写文本
p.read_bytes()                   # 读二进制

# 遍历目录
for item in Path("mydir").iterdir():       # 只一层
    print(item.name)

for item in Path("mydir").glob("**/*.json"):  # 递归找所有 json
    print(item)
```

> **建议：** 新代码统一用 `pathlib`。遇到老代码用 `os.path` 能读懂即可。

---

## 三、JSON 处理

### 3.1 核心方法

```python
import json

# 字符串 ↔ 对象
data = json.loads('{"name": "张三", "age": 22}')   # str → dict
json_str = json.dumps(data)                          # dict → str

# 文件 ↔ 对象
with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)            # 读文件 → dict

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f)             # dict → 写文件
```

### 3.2 dumps/dump 常用参数

```python
import json

data = {"name": "张三", "age": 22, "tags": ["Python", "AI"]}

# 格式化输出（人类可读）
print(json.dumps(data, indent=2, ensure_ascii=False))
# {
#   "name": "张三",
#   "age": 22,
#   "tags": ["Python", "AI"]
# }

# sort_keys: 按 key 排序（方便 git diff）
print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

# ensure_ascii=False → 中文直接显示，而不是 张三
```

> **坑点：** `json.dumps` 默认 `ensure_ascii=True`，中文会变成 `\uXXXX`。写日志/配置文件一定要 `ensure_ascii=False`。

### 3.3 嵌套结构读写

```python
# 读取嵌套 JSON
with open("nested.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 安全取值 —— 层层判空 or 用 try
try:
    city = data["user"]["profile"]["address"]["city"]
except (KeyError, TypeError):
    city = "未知"

# 更好的写法（Python 3.8+ 海象运算符 or 用 .get）
city = (((data.get("user") or {}).get("profile") or {}).get("address") or {}).get("city", "未知")
```

---

## 四、CSV 处理

### 4.1 csv.reader / csv.writer（基础）

```python
import csv

# 读 CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)   # 跳过表头
    for row in reader:
        # row 是 list[str]，如 ["张三", "22", "北京"]
        print(row[0], row[1])

# 写 CSV
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄", "城市"])   # 写表头
    writer.writerow(["张三", "22", "北京"])
    writer.writerows([                          # 批量写
        ["李四", "25", "上海"],
        ["王五", "28", "深圳"],
    ])
```

> **坑点：** Windows 下写 CSV 必须加 `newline=""`，否则每行之间会多一个空行。

### 4.2 csv.DictReader / csv.DictWriter（推荐）

```python
import csv

# 读 —— 每行是 dict，key 来自表头
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # row → {"姓名": "张三", "年龄": "22", "城市": "北京"}
        print(row["姓名"])

# 写
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"name": "张三", "age": 22, "city": "北京"})
    writer.writerows([
        {"name": "李四", "age": 25, "city": "上海"},
        {"name": "王五", "age": 28, "city": "深圳"},
    ])
```

> **建议：** 能用 `DictReader/DictWriter` 就不用 `reader/writer`——代码可读性高很多。

---

## 五、实战练习

### 练习 1（入门）：JSON 配置文件解析 → 写入 CSV

**要求：** 写一个脚本，在 `C:\Users\Administrator\python-learning\` 下创建以下 JSON 文件，然后读取并转成 CSV。

```python
"""ex1_json_to_csv.py — 读取 JSON 配置，提取所有字段写入 CSV"""
import json
import csv
from pathlib import Path

BASE = Path(r"C:\Users\Administrator\python-learning")

# ============================================================
# 第 1 步：创建示例 JSON 文件（自己跑一遍感受一下）
# ============================================================
sample_config = {
    "app_name": "MyAgent",
    "version": "1.0.0",
    "settings": {
        "model": "claude-sonnet-4-6",
        "temperature": 0.7,
        "max_tokens": 4096
    },
    "tools": [
        {"name": "search", "enabled": True},
        {"name": "calculator", "enabled": False},
        {"name": "file_reader", "enabled": True}
    ]
}

config_path = BASE / "day4_config.json"
config_path.write_text(
    json.dumps(sample_config, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print(f"✅ 已创建示例 JSON：{config_path}")

# ============================================================
# 第 2 步：读取 JSON，展平写出 CSV
# ============================================================
# 读入
data = json.loads(config_path.read_text(encoding="utf-8"))

# 展平为键值对列表
rows = [
    ["path", "value"],
    ["app_name", data["app_name"]],
    ["version", data["version"]],
    ["settings.model", data["settings"]["model"]],
    ["settings.temperature", data["settings"]["temperature"]],
    ["settings.max_tokens", data["settings"]["max_tokens"]],
]
for i, tool in enumerate(data["tools"], 1):
    rows.append([f"tools.{i}.name", tool["name"]])
    rows.append([f"tools.{i}.enabled", tool["enabled"]])

# 写 CSV
csv_path = BASE / "day4_config.csv"
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"✅ 已导出 CSV：{csv_path}")
```

---

### 练习 2（中等）：遍历目录统计文件类型

**要求：** 写一个脚本，递归遍历指定目录（比如 `C:\Users\Administrator\python-learning\`），统计每种文件扩展名的数量和总大小。

```python
"""ex2_file_stats.py — 递归遍历目录，统计文件类型"""
from pathlib import Path
from collections import defaultdict

TARGET = Path(r"C:\Users\Administrator\python-learning")

# 如果目录为空，先造一些测试文件
if not list(TARGET.iterdir()):
    (TARGET / "notes.md").write_text("# 笔记\n内容", encoding="utf-8")
    (TARGET / "data.json").write_text('{"key": "value"}', encoding="utf-8")
    (TARGET / "data.csv").write_text("name,age\n张三,22\n", encoding="utf-8")
    (TARGET / "image.png").write_bytes(b"\x89PNG placeholder")
    sub = TARGET / "subdir"
    sub.mkdir(exist_ok=True)
    (sub / "readme.md").write_text("# 子目录", encoding="utf-8")
    (sub / "another.json").write_text("[1, 2, 3]", encoding="utf-8")
    print("✅ 已创建测试文件\n")

# 统计
stats = defaultdict(lambda: {"count": 0, "size": 0})  # 默认值工厂

for item in TARGET.rglob("*"):
    if item.is_file():
        ext = item.suffix or "(无后缀)"
        stats[ext]["count"] += 1
        stats[ext]["size"] += item.stat().st_size

# 输出结果
print(f"{'扩展名':<12} {'数量':>6} {'总大小(字节)':>14}")
print("-" * 35)
for ext, info in sorted(stats.items()):
    print(f"{ext:<12} {info['count']:>6} {info['size']:>14,}")

total_files = sum(s["count"] for s in stats.values())
total_size = sum(s["size"] for s in stats.values())
print("-" * 35)
print(f"{'合计':<12} {total_files:>6} {total_size:>14,}")
```

---

### 练习 3（进阶）：CSV → JSON 转换（带数据清洗）

**要求：** 读入一个 CSV 文件（模拟脏数据），清洗后转成 JSON 输出。

```python
"""ex3_csv_to_json.py — 读脏 CSV，清洗，写 JSON"""
import csv
import json
from pathlib import Path

BASE = Path(r"C:\Users\Administrator\python-learning")

# ============================================================
# 第 1 步：制造一份"脏"CSV（有空行、多余空格、缺失值）
# ============================================================
dirty_csv = BASE / "day4_dirty.csv"
dirty_csv.write_text("""\
姓名,年龄,城市,邮箱
张三,22,北京,zhangsan@mail.com
李四,25,,lisi@mail.com
  王五  ,  二十八  ,深圳,wangwu@
,30,上海,xiaoming@mail.com
赵六,-5,广州,zhaoliu@mail.com
""", encoding="utf-8")

# ============================================================
# 第 2 步：读取 + 清洗
# ============================================================
cleaned = []

with open(dirty_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=2):  # start=2 因为第 1 行是表头
        # 清洗：去掉所有值的前后空格
        row = {k: v.strip() for k, v in row.items()}

        errors = []

        # 校验姓名：不能为空
        if not row["姓名"]:
            errors.append("姓名为空")
        # 校验年龄：必须是数字且 >= 0
        try:
            age = int(row["年龄"])
            if age < 0:
                errors.append(f"年龄为负数({age})")
            row["年龄"] = age  # 转成 int
        except ValueError:
            errors.append(f"年龄不是数字({row['年龄']})")

        # 校验邮箱：包含 @（简化验证）
        if "@" not in row["邮箱"]:
            errors.append(f"邮箱格式错误({row['邮箱']})")

        if errors:
            print(f"⚠️  第{i}行跳过 — {'; '.join(errors)}")
            continue

        cleaned.append(row)

# ============================================================
# 第 3 步：写出 JSON
# ============================================================
output_path = BASE / "day4_cleaned.json"
output_path.write_text(
    json.dumps(cleaned, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"\n✅ 清洗完成：{len(cleaned)} 条有效数据 → {output_path}")
```

预期输出：
```
⚠️  第3行跳过 — 城市为空
⚠️  第4行跳过 — 年龄不是数字(二十八); 邮箱格式错误(wangwu@)
⚠️  第6行跳过 — 姓名不能为空; 年龄为负数(-5)

✅ 清洗完成：2 条有效数据 → .../day4_cleaned.json
```

---

## 今日检验清单

今天学完后，你应该能：

- [ ] 用 `with open(..., 'r', encoding='utf-8')` 安全读写文件
- [ ] 用 `pathlib.Path` 做路径拼接和遍历
- [ ] 用 `json.load/dump/loads/dumps` 序列化/反序列化
- [ ] 用 `csv.DictReader/DictWriter` 读写 CSV
- [ ] 写一个脚本：读文件 → 处理数据 → 写出结果

---

> **下一步：** Day 5 学虚拟环境 venv + pip，然后进入 async/await 异步编程。文件 IO 是后续所有项目的基础——数据摄入、日志、配置读写都靠它。

---

## 附：Windows 终端编码问题

Windows 默认终端编码是 GBK，`print()` 中文或 emoji 可能报错：

```
UnicodeEncodeError: 'gbk' codec can't encode character ...
```

**解决：** 运行时加环境变量

```bash
# Git Bash / PowerShell
PYTHONIOENCODING=utf-8 python your_script.py
```

或者在脚本**最开头**加上：

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```
