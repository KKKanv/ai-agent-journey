import re
class WordCounter:
    def __init__(self, text: str):
        self.words = re.findall(r'\b\w+\b', text.lower())
        self.freq = {}
        for word in self.words:
            self.freq[word] = self.freq.get(word, 0) + 1

    def count(self) -> int:
        return len(self.words)

    def frequency(self) -> dict:
        return self.freq.copy()

    def top_n(self, n: int) -> list:
        return sorted(self.freq.items(), key=lambda x: x[1], reverse=True)[:n]
