"""
    内置高阶函数
"""
from common2.list_helper import ListHelper


class Wife:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


list01 = [
    Wife("翠花", 36, 60, 1.5),
    Wife("如花", 39, 75, 1.3),
    Wife("赵敏", 25, 46, 1.7),
    Wife("灭绝", 42, 50, 1.8)
]
list02 = [
    Wife("翠花2", 36, 60, 1.5),
    Wife("如花2", 39, 75, 1.3),
    Wife("赵敏2", 25, 46, 1.7),
    Wife("灭绝2", 42, 50, 1.8)
]
"""
    filter
    语法:
        filter(函数，可迭代对象)
    作用:
        根据条件筛选可迭代对象中的元素，返回值为新可迭代对象
    和自己写的 list_helper 中的 find_all 原理一样
"""
print("-----filter-----")
# 自己定义
for item in ListHelper.find_all(list01, lambda item: item.age < 40):
    print(item.name)

# 1. 过滤:根据条件筛选可迭代对象中的元素，返回值为新可迭代对象。
for item in filter(lambda item: item.age < 40, list01):
    print(item.name)

"""
    map
    map（函数，可迭代对象）：使用可迭代对象中的每个元素调用函数，将返回值作为新可迭代对象元素；返回值为新可迭代对象。

    与 list_helper 中的 select 一样
"""
print("-----map-----")
# 自己定义
for item in ListHelper.select(list01, lambda item: (item.name, item.age)):
    print(item)

# 2. 映射:使用可迭代对象中的每个元素调用函数，将返回值作为新可迭代对象元素；
for item in map(lambda item: (item.name, item.age), list01):
    print(item)
print("*****")
# 多个可迭代对象时，需要对应数量的形参
for item in map(lambda item, item2: (item.name, item2.age), list01, list02):
    print(item)

"""

    sorted
    sorted(可迭代对象，key = 函数,reverse = bool值)：排序，返回值为排序结果
    
    与 list_helper 中的 order_by 原理一样，但是返回的是新的序列，原来的序列不改变
    key 即 函数条件
    reverse 反转，默认升序排序
    
"""

print("----sorted-----")
# 自己定义
# ListHelper.order_by(list01, lambda item: item.height)
# for item in list01:
#     print(item.height)

# 3. 排序(返回排序结果,支持升序与降序),原序列不影响
# 升序排列
for item in sorted(list01, key=lambda item: item.height):
    print(item.height)

# 降序排列
for item in sorted(list01, key=lambda item: item.height, reverse=True):
    print(item.height)

"""

min 
max

    类似 list_helper 中的 get_max 原理一样
"""
print("--min max---")
# 自己定义
re = ListHelper.get_max(list01,lambda item: item.weight)
print(re.name)

# 4. 获取最大值
re = max(list01, key=lambda item: item.weight)
print(re.name)

# 5. 获取最小值
re = min(list01, key=lambda item: item.weight)
print(re.name)




# 使用 方法参数 测试

def fun01(item):
    return item.atk


class Skill:
    def __init__(self, id=0, name="", atk=0, duration=0.1):
        self.id = id
        self.name = name
        self.atk = atk
        self.duration = duration


list01 = [
    Skill(101, "葵花宝典", 850, 10),
    Skill(102, "辟邪剑法", 800, 5),
    Skill(103, "狮吼功", 500, 8),
    Skill(104, "降龙十八掌", 700, 3),
    Skill(105, "电炮飞脚", 8, 2),
]


re = min(list01, key=fun01)
print(re.name)

