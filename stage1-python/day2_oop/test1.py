def describe_student(name,age,**kwargs):
    base=f"{name},{age}岁"
    extra_parts=[f"{key}:{value}" for key,value in kwargs.items()]
    extra=",".join(extra_parts)

    if extra:
        print(f"{base}|{extra}")
    else: print(base)

describe_student("张三", 21, score=92, city="杭州", hobby="coding")