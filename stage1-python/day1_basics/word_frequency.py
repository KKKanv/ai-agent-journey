import re
from pathlib import Path

def count_words(text: str) -> dict[str, int]:
    text = text.lower()
    words = re.findall(r"[a-zA-Z]+", text)
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def print_top(freq: dict[str, int], n: int = 100) -> None:
    sorted_items = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    print(f"{'排名':<6}{'单词':<20}{'次数':<6}")
    print("-" * 32)
    for rank, (word, count) in enumerate(sorted_items[:n], start=1):
        print(f"{rank:<6}{word:<20}{count:<6}")

def main():
    file_path = Path(__file__).parent / "傲慢与偏见原文.txt"
    if not file_path.exists():
        print(f"找不到文件: {file_path}")
        print("请在同目录下创建一个 sample.txt 文件（粘贴一段英文文章即可）")
        return
    text = file_path.read_text(encoding="utf-8")
    freq = count_words(text)
    print(f"\n总单词数: {sum(freq.values())} 种\n")
    print_top(freq, n=20)

if __name__ == "__main__":
    main()