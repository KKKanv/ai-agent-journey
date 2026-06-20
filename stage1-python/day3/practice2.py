#题目：
#  1. 用 sorted() + lambda，按单词长度升序排序 words
#  2. 用 sorted() + lambda，按单词字母序排序（忽略大小写）words
#  3. 用 sorted() + lambda，按分数降序排序 pairs
#  4. 用 filter() + lambda，从 words 中选出长度 ≥ 5 的单词
#  5. 用 map() + lambda，把 pairs 转成 ["Alice:88", "Bob:92", ...]

# 数据准备 
words = ["apple", "Banana", "cherry", "Date", "elderberry", "Fig", "grape"]
pairs = [("Alice", 88), ("Bob", 92), ("Charlie", 75), ("Diana", 95)]

#1.
print(sorted(words,key=lambda a:len(a)))
#2.
print(sorted(words,key=lambda w:w.lower()))
#3.
print(sorted(pairs,key=lambda x:x[1],reverse=True))
#4.
print(list(filter(lambda w:len(w) >=5,words)))
#5.
print(list(map(lambda p:f"{p[0]}:{p[1]}",pairs)))