"""练习2：递归遍历目录，统计文件类型

遍历指定目录（含子目录），统计每种扩展名的文件数量和总大小。
"""
from pathlib import Path
from collections import defaultdict

TARGET = Path(r"D:\Transform\ai-agent-journey\stage1-python\day4")


def create_test_files():
    """如果目录为空，创建一些测试文件"""
    if list(TARGET.iterdir()):
        return  # 已有文件，跳过

    (TARGET / "notes.md").write_text("# 笔记\n今天学习了文件IO", encoding="utf-8")
    (TARGET / "data.json").write_text('{"key": "value", "number": 42}', encoding="utf-8")
    (TARGET / "data.csv").write_text("name,age,city\n张三,22,北京\n李四,25,上海\n", encoding="utf-8")
    (TARGET / "image.png").write_bytes(b"\x89PNG\x0d\x0a\x1a\x0aplaceholder")
    (TARGET / "no_extension").write_text("无后缀的文件", encoding="utf-8")

    sub = TARGET / "subdir"
    sub.mkdir(exist_ok=True)
    (sub / "readme.md").write_text("# 子目录中的文件", encoding="utf-8")
    (sub / "another.json").write_text('[1, 2, 3, "hello"]', encoding="utf-8")

    print("[OK] 已创建测试文件\n")


def scan_directory(root: Path):
    """递归扫描目录，统计文件类型"""
    stats = defaultdict(lambda: {"count": 0, "size": 0})

    for item in root.rglob("*"):
        if item.is_file():
            ext = item.suffix.lower() or "(无后缀)"
            stats[ext]["count"] += 1
            stats[ext]["size"] += item.stat().st_size

    return stats


def print_report(stats: dict):
    """格式化输出统计报告"""
    print(f"{'扩展名':<12} {'数量':>6} {'总大小(字节)':>14} {'占比':>8}")
    print("-" * 44)

    total_size = sum(s["size"] for s in stats.values())
    total_files = sum(s["count"] for s in stats.values())

    for ext, info in sorted(stats.items(), key=lambda x: x[1]["size"], reverse=True):
        pct = (info["size"] / total_size * 100) if total_size > 0 else 0
        print(f"{ext:<12} {info['count']:>6} {info['size']:>14,} {pct:>7.1f}%")

    print("-" * 44)
    print(f"{'合计':<12} {total_files:>6} {total_size:>14,}  {'100.0%':>7}")


if __name__ == "__main__":
    create_test_files()
    stats = scan_directory(TARGET)
    print_report(stats)
