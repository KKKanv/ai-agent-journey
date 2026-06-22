"""练习1：JSON 配置文件解析 → 写入 CSV

读取一个 JSON 配置文件，将嵌套结构展平为键值对，输出 CSV。
"""
import json
import csv
from pathlib import Path

BASE = Path(r"D:\Transform\ai-agent-journey\stage1-python\day4")


def create_sample_json():
    """第 1 步：创建示例 JSON 文件"""
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
    print(f"[OK] 已创建示例 JSON：{config_path}")
    return config_path


def flatten_and_export(config_path: Path):
    """第 2 步：读取 JSON，展平为键值对，写出 CSV"""
    data = json.loads(config_path.read_text(encoding="utf-8"))

    # 展平嵌套结构
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

    csv_path = BASE / "day4_config.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"[OK] 已导出 CSV：{csv_path}")

    # 打印预览
    print("\n--- CSV 内容预览 ---")
    for row in rows:
        print(f"  {row[0]:<25} {row[1]}")


if __name__ == "__main__":
    path = create_sample_json()
    flatten_and_export(path)
