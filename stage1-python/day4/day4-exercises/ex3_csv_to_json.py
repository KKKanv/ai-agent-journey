"""练习3：CSV → JSON 转换（带数据清洗）

读入一份"脏"CSV（有空行、空格、格式错误、缺失值），清洗后写出 JSON。
"""
import csv
import json
from pathlib import Path

BASE = Path(r"D:\Transform\ai-agent-journey\stage1-python\day4")


def create_dirty_csv():
    """制造一份带脏数据的 CSV"""
    dirty_csv = BASE / "day4_dirty.csv"
    dirty_csv.write_text("""\
姓名,年龄,城市,邮箱
张三,22,北京,zhangsan@mail.com
李四,25,,lisi@mail.com
  王五  ,  二十八  ,深圳,wangwu@
,30,上海,xiaoming@mail.com
赵六,-5,广州,zhaoliu@mail.com
""", encoding="utf-8")
    print(f"[OK] 已创建脏数据 CSV：{dirty_csv}")
    print("  (包含：空格污染、非数字年龄、空姓名、负数年龄、无效邮箱)\n")
    return dirty_csv


def clean_and_validate(csv_path: Path) -> list[dict]:
    """读取 CSV，逐行清洗校验，返回有效数据列表"""
    cleaned = []
    errors_log = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            # ---- 清洗：去掉前后空格 ----
            row = {k: v.strip() for k, v in row.items()}

            errors = []

            # 校验 1：姓名不能为空
            if not row["姓名"]:
                errors.append("姓名为空")

            # 校验 2：年龄必须是 >=0 的整数
            try:
                age = int(row["年龄"])
                if age < 0:
                    errors.append(f"年龄为负数({age})")
                else:
                    row["年龄"] = age  # 转成 int 存储
            except ValueError:
                errors.append(f"年龄不是数字('{row['年龄']}')")

            # 校验 3：邮箱必须包含 @
            if not row["邮箱"] or "@" not in row["邮箱"]:
                errors.append(f"邮箱格式错误('{row['邮箱']}')")

            # 校验 4：城市缺失（warn 但不跳过）
            if not row["城市"]:
                row["城市"] = "未知"

            if errors:
                errors_log.append((i, errors))
                continue

            cleaned.append(row)

    # 打印清洗日志
    for line_no, errs in errors_log:
        print(f"[WARN] 第{line_no}行跳过 -> {'; '.join(errs)}")

    return cleaned


def export_json(data: list[dict]):
    """写出 JSON 文件"""
    output_path = BASE / "day4_cleaned.json"
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"\n[OK] 清洗完成：{len(data)} 条有效数据")
    print(f"   输出文件：{output_path}")

    # 预览
    if data:
        print("\n--- 清洗结果预览 ---")
        for row in data:
            print(f"   {row['姓名']}, {row['年龄']}, {row['城市']}, {row['邮箱']}")


if __name__ == "__main__":
    csv_path = create_dirty_csv()
    valid_data = clean_and_validate(csv_path)
    export_json(valid_data)
