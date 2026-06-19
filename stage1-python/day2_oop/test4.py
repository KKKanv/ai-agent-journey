class Student:
    def __init__(self, name: str, score: int, grade: str):
        self.name = name
        self.score = score
        self.grade = grade

    def __str__(self) -> str:
        """返回格式：'张三(大三): 92分'"""
        return f"{self.name}({self.grade}): {self.score}分"

    def __lt__(self, other: 'Student') -> bool:
        """按分数比较，分数低的 '小于' 分数高的（用于排序）"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.score < other.score

    def __eq__(self, other: object) -> bool:
        """同姓名且同年级视为相等（分数不计入相等比较）"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.name == other.name and self.grade == other.grade

    # 可选：为了 completeness，可以同时实现 __gt__、__le__ 等，
    # 但 Python 会自动根据 __lt__ 和 __eq__ 进行补充，所以不必须。