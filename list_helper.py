"""
    静态方法
    工具类: 定义针对可迭代对象的常用操作
"""

"""
    类似
    微软 LINQ  语言集成查询框架
     集成操作框架
"""
class ListHelper:
    """
        列表助手类
    """

    @staticmethod
    def find_all(iterable, func_condition):
        """
        根据指定条件,在可迭代对象中查找多个元素

        :param iterable: 可迭代对象(字典返回键)
        :param func_condition: 查找条件(函数类型)
               func_condition( iterable中的元素 ) --> bool
        :return: 所有满足的条件的元素
        """
        for item in iterable:
            if func_condition(item):
                yield item

    @staticmethod
    def find_single(iterable, func_condition):
        """
        根据指定条件,在可迭代对象中查找单个元素

        :param iterable: 可迭代对象(字典返回键)
        :param func_condition: 查找条件(函数类型)
        func_condition( iterable中的元素 ) --> bool
        :return: 第一个满足的条件的元素
        """
        for item in iterable:
            if func_condition(item):
                return item

    @staticmethod
    def get_count(iterable, func_condition):
        """
        根据指定条件,在可迭代对象中查找符合条件的元素个数

        :param iterable: 可迭代对象(字典返回键)
        :param func_condition: 查找条件(函数类型)
        func_condition( iterable中的元素 ) --> bool
        :return: 满足条件的元素个数
        """
        count = 0
        for item in iterable:
            if func_condition(item):
                count += 1
        return count

    @staticmethod
    def is_exists(iterable, func_condition):
        """
        根据指定条件,在可迭代对象中是否存在符合条件的元素

        :param iterable: 可迭代对象(字典返回键)
        :param func_condition: 查找条件(函数类型)
        func_condition( iterable中的元素 ) --> bool
        :return: 是否存在 True表示存在,False表示不存在
        """
        for item in iterable:
            if func_condition(item):
                return True
        return False

    @staticmethod
    def sum(iterable, func_condition):
        """
             在可迭代对象中根据指定条件进行求和计算
         :param iterable:需要求和的可迭代对象
         :param func_condition: 函数类型的求和条件
               func_condition(可迭代对象中的元素) --> 任意类型
         :return:求和的结果
         """
        sum_result = 0
        for item in iterable:
            sum_result += func_condition(item)
        return sum_result

    @staticmethod
    def select(iterable, func_condition):
        """
             在可迭代对象中根据指定条件对每个元素进行筛选
         :param iterable:需要筛选的可迭代对象
         :param func_condition: 函数类型的筛选条件
               func_condition(可迭代对象中的元素) --> 任意类型
         :return:生成器对象类型的筛选结果
         """
        for item in iterable:
            yield func_condition(item)

    @staticmethod
    def get_max(iterable, func_condition):
        """
             在可迭代对象中根据指定条件获取最大元素
         :param iterable:需要搜索的可迭代对象
         :param func_condition: 函数类型的搜索条件
               func_condition(可迭代对象中的元素) --> 任意类型
         :return:最大元素
         """
        max_item = iterable[0]
        for i in range(1, len(iterable)):
            if func_condition(iterable[i]) > func_condition(max_item):
                max_item = iterable[i]
        return max_item

    @staticmethod
    def order_by(iterable, func_condition):
        """
             根据指定条件对可迭代对象进行升序排列
         :param iterable:需要排序的可迭代对象
         :param func_condition: 函数类型的排序依据
               func_condition(可迭代对象中的元素) --> 任意类型
         """
        for row in range(len(iterable) - 1):
            for col in range(row + 1, len(iterable)):
                if func_condition(iterable[row]) > func_condition(iterable[col]):
                    iterable[row], iterable[col] = iterable[col], iterable[row]
