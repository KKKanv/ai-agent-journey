
users = [
      {"name": "Alice", "age": 25, "score": 88},
      {"name": "Bob", "age": 17, "score": 92},
      {"name": "Charlie", "age": 30, "score": 75},
      {"name": "Diana", "age": 22, "score": 95},
      {"name": "Eve", "age": 16, "score": 85},
  ]
#题目：
# 1. 用列表推导式，取出所有 age >= 18 的用户名字 → ['Alice', 'Charlie', 'Diana']
# 2. 用字典推导式，构造 {名字: score} 的字典（仅限分数 ≥ 85 的人）
# 3. 用集合推导式，收集所有人的年龄 → {25, 17, 30, 22, 16}
# 4. （进阶）用嵌套推导式，把 [[1, 2], [3, 4], [5, 6]] 拍平成 [1, 2, 3, 4, 5, 6]

#练习题一 1.
print(res:=[user["name"] for user in users if user["age"]>=18])
#练习题一 2.
print (res:={user["name"]:user["score"] for user in users if user["score"]>=85})
#练习题一 3.
print(res:={user["age"] for user in users})
#练习题一 4.
temp=[[1, 2], [3, 4], [5, 6]]
print(res:=[num for list in temp for num in list])