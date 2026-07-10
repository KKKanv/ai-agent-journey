"""
练习 3：pip vs conda 对比体验

目标：用 pip 装一个包，再用 conda 创建环境，感受差异。

前置条件：已安装 Miniconda / Anaconda（如果没有，可以跳过 conda 部分）

步骤 A — pip 体验（在刚刚的 venv 中）：

    (venv) $ python day5-exercises/exercise3_compare.py

步骤 B — conda 体验（如果已安装 conda，新建一个终端执行）：

    # 创建 conda 环境（指定 Python 3.10）
    conda create -n ai-journey python=3.10 -y

    # 激活
    conda activate ai-journey

    # 安装 numpy
    conda install numpy -y

    # 查看 Python 版本
    python --version

    # 查看环境路径
    which python          # Linux/macOS
    where python          # Windows

    # 退出
    conda deactivate

    # 查看所有环境
    conda env list

    # 清理（可跳过）
    # conda remove -n ai-journey --all -y

对比思考：
    - pip 版安装 numpy 多大？conda 版安装多大？
    - conda 会自动装什么系统依赖？
"""

import sys
import importlib

print(f"当前 Python 路径: {sys.executable}")
print()

# 检查能否导入 numpy（确认在正确的 venv 中运行）
for pkg_name in ["requests", "numpy"]:
    try:
        mod = importlib.import_module(pkg_name)
        print(f"✅ {pkg_name} == {mod.__version__}  — 导入成功！")
    except ImportError:
        print(f"❌ {pkg_name} 未安装 — 用 pip install {pkg_name}")

print()
print("—" * 40)
print("💡 提示：对比 conda 环境，看看环境路径是否不同。")
print("尝试在当前环境：pip list | findstr numpy")
print("在 conda 环境：  conda list numpy")
