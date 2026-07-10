# Day 5: 虚拟环境 + pip 包管理

> 第一阶段 Python 速通 — 第五天  
> 目标：掌握 Python 项目依赖管理，学会用虚拟环境隔离不同项目

---

## 1. 为什么需要虚拟环境？

### 痛点场景

```
项目 A：依赖 Flask 2.0（兼容 Python 3.8+）
项目 B：依赖 Flask 3.0（需要 Python 3.9+，且 API 变了）
       ↓
全局装一个 Flask → 总有一个项目跑不起来 💥
```

### 虚拟环境解决什么

| 问题 | 方案 |
|------|------|
| 不同项目依赖不同版本 | 每个项目独立环境 |
| 系统 Python 被改乱 | 虚拟环境不影响全局 |
| 部署时知道装什么 | `requirements.txt` 精确锁定 |
| 多人协作统一环境 | 共享一份依赖清单 |

### 核心思想

> **每个项目拥有独立的 Python 解释器 + 包目录，互不干扰。**

---

## 2. venv — Python 自带虚拟环境

Python 3.3+ 内置 `venv` 模块，**无需额外安装**。

### 2.1 创建虚拟环境

```bash
# 在项目目录下创建
python -m venv venv
#                    ↑ 环境名（惯例就叫 venv，方便 .gitignore）
```

执行后生成 `venv/` 文件夹，包含：
```
venv/
├── Scripts/        # 激活脚本、Python 可执行文件
│   ├── activate    # (bash)
│   ├── activate.bat  # (cmd)
│   └── Activate.ps1  # (PowerShell)
├── Lib/site-packages/  # 第三方包安装到这里
└── pyvenv.cfg      # 配置文件（指向系统 Python）
```

### 2.2 激活环境

```bash
# Git Bash / Linux / macOS
source venv/Scripts/activate

# 或简写
. venv/Scripts/activate

# Windows CMD
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1
```

**激活后可以看到提示符变化：**
```bash
(venv)  # ← 前面出现环境名
user@pc:~/project$
```

### 2.3 验证是否在虚拟环境中

```bash
which python   # Linux/macOS
# 应输出: .../venv/Scripts/python  (不是 /usr/bin/python)

where python  # Windows
# 应输出: .../venv/Scripts/python.exe

python -c "import sys; print(sys.executable)"
# 应指向 venv 内部的 python
```

### 2.4 退出环境

```bash
deactivate
```

### 2.5 删除环境

```bash
# 直接删文件夹
rm -rf venv/          # Linux/macOS/Git Bash
rmdir /s venv\        # Windows CMD
```

> ⚠️ 只删环境，**不影响项目代码**。重新 `python -m venv venv` 即可重建。

---

## 3. pip — Python 包管理器

### 3.1 常用命令速查

| 命令 | 作用 |
|------|------|
| `pip install <包名>` | 安装包 |
| `pip install <包名>==1.2.3` | 安装**指定版本** |
| `pip install <包名>>=1.0,<2.0` | 安装版本范围 |
| `pip install -r requirements.txt` | 批量安装（从文件） |
| `pip uninstall <包名>` | 卸载包 |
| `pip list` | 列出所有已安装包 |
| `pip freeze` | 列出已安装包 + **精确版本号** |
| `pip show <包名>` | 查看包详情 |
| `pip search <关键词>` | 搜索包（已废弃，去 pypi.org 搜） |

### 3.2 pip freeze — 最重要的命令

```bash
# 导出当前环境所有依赖（带精确版本）
pip freeze > requirements.txt
```

生成的文件内容示例：
```
requests==2.31.0
numpy==1.24.3
flask==3.0.0
```

### 3.3 requirements.txt 最佳实践

```txt
# 这是注释
requests==2.31.0          # 精确锁定（推荐给生产环境）
numpy>=1.24,<2.0          # 版本范围（灵活度高）
flask                     # 不指定版本 = 最新版（不推荐）
```

**别人拿到项目后：**
```bash
python -m venv venv
source venv/Scripts/activate   # 先激活
pip install -r requirements.txt # 一键安装所有依赖
```

### 3.4 pip 常用选项

| 选项 | 作用 |
|------|------|
| `-i https://pypi.tuna.tsinghua.edu.cn/simple` | 指定国内镜像源（加速下载） |
| `--upgrade` / `-U` | 升级包 |
| `--user` | 安装到用户目录（**不推荐** vs venv） |
| `--no-deps` | 只安装包本身，不装依赖 |

**配置永久镜像源：**
```bash
# 全局配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 查看当前配置
pip config list
```

---

## 4. conda — 更重量级的环境管理

### 4.1 venv vs conda 对比

| 特性 | venv | conda |
|------|------|-------|
| 随 Python 自带 | ✅ 是 | ❌ 需要装 Anaconda/Miniforge |
| 只管理 Python 包 | ✅ | ❌ 可管理**任何软件**（R、C++ 库等） |
| 环境切换速度 | 快（秒级） | 中等 |
| 磁盘占用 | 小（共享系统级 .pyc） | 大（每个环境独立） |
| 非 Python 依赖 | ❌ 需系统包管理器 | ✅ conda 直接装（如 cudatoolkit） |
| 适用场景 | 纯 Python 项目 | 数据科学 / 需要系统库的项目 |

### 4.2 conda 常用命令

```bash
# 创建环境
conda create -n myenv python=3.10

# 激活环境
conda activate myenv

# 退出环境
conda deactivate

# 安装包
conda install numpy pandas

# 列出所有环境
conda env list

# 删除环境
conda remove -n myenv --all

# 导出环境
conda env export > environment.yml

# 从 yml 创建环境
conda env create -f environment.yml
```

### 4.3 pip + conda 混用注意事项

```bash
# 最佳顺序：
conda install numpy pandas    # 1. conda 装（能处理系统依赖）
pip install flask requests    # 2. pip 装（conda 没有的纯 Python 包）

# ❌ 不要：先 pip 装大量包，再用 conda
# ❌ 不要：两个混着装同一包
```

---

## 5. .gitignore — 千万别把环境提交上去

### 必须忽略的

```gitignore
# 虚拟环境
venv/
.venv/
env/

# Python 缓存
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# 系统文件
.DS_Store
Thumbs.db
```

> **为什么不能提交 venv？**  
> 1. 体积大（几十 MB）  
> 2. 跨平台不兼容（Windows/Linux 的 .exe 不同）  
> 3. 依赖定义在 `requirements.txt` 里就够了  
> 4. 别人 `pip install -r requirements.txt` 就能复现

---

## 6. 完整工作流演示

```bash
# 1. 克隆项目
git clone https://github.com/xxx/my-project.git
cd my-project

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活
source venv/Scripts/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 开发 ...
pip install new-package     # 装新包
pip freeze > requirements.txt  # 更新依赖清单

# 6. 退出
deactivate
```

---

## 7. 常见问题

### Q: `pip` 命令找不到？
```bash
python -m pip install requests   # 用 python -m pip 代替
```

### Q: `pip list` 显示的是全局包？
→ 没有激活虚拟环境。激活后重新检查。

### Q: 激活后 `python` 还是系统版本？
→ 检查是否在正确的 shell 中，确认 `which python` 路径。

### Q: Windows 上 `venv\Scripts\activate` 报权限错误？
```powershell
# PowerShell 以管理员运行
Set-ExecutionPolicy Unrestricted -Scope Process
# 再试
venv\Scripts\Activate.ps1
```

---

## 总结

```
✅ 虚拟环境 = 项目隔离，避免依赖冲突
✅ venv 是 Python 自带，轻量够用
✅ pip freeze > requirements.txt 锁定依赖
✅ .gitignore 忽略 venv/ 目录
✅ conda 更强，但纯 Python 项目 venv 足矣
```
