"""
练习 1：创建虚拟环境 + 安装包 + 导出依赖

目标：熟悉 venv 创建、pip 安装、requirements.txt 导出的完整流程。

步骤（请在终端手动执行，不是运行这个 .py 文件）：

    # 1. 在 day5_venv_pip/ 目录下创建虚拟环境
    python -m venv venv

    # 2. 激活环境
    source venv/Scripts/activate        # Git Bash
    # 或 venv\Scripts\activate          # Windows CMD

    # 3. 安装包
    pip install requests numpy

    # 4. 验证安装
    pip list

    # 5. 导出依赖
    pip freeze > requirements.txt

    # 6. 查看生成的文件
    cat requirements.txt                # Git Bash
    # 或 type requirements.txt          # CMD

    # 7. 退出环境
    deactivate

完成后，你的 requirements.txt 应该类似：
    certifi==2024.12.14
    charset-normalizer==3.3.2
    idna==3.6
    numpy==1.26.4
    requests==2.31.0
    urllib3==2.1.0

注意：以上版本号仅供参考，实际以你安装时的最新版为准。
"""
print("练习 1 ← 请在终端手动执行上述步骤，不是运行这个文件。")
print("先激活虚拟环境，然后：pip install requests numpy")
