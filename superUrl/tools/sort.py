# 对数据列表根据星级下载数进行排序
# 1下载数等于3.5星

#
# data_list = [{'name': 'aaa',
#               'download_count': 0,
#               'star_one': 0,
#               'star_two': 0,
#               'star_three': 0,
#               'star_four': 0,
#               'star_five': 0,
#               'star_avg': 0,
#               'url': 'iii'},
#              {'name': 'aaa',
#               'download_count': 0,
#               'star_one': 0,
#               'star_two': 0,
#               'star_three': 0,
#               'star_four': 0,
#               'star_five': 0,
#               'star_avg': 0,
#               'url': 'iii'},
#              ]

def query_sort(data_list,low,high):
    if low < high:
        k = sort(data_list,low,high)

        query_sort(data_list,low,k-1)

        query_sort(data_list,k+1,high)

    return data_list[::-1]


def count_grate(item):
    downloads = int(item['download_count'])
    stars = int(item['star_one'])+ int(item['star_two']) + int(item['star_three']) + int(item['star_four']) + int(item['star_five'])
    count = downloads + stars
    if count == 0:
        return 0
    total_grade = (downloads * 3.5 + stars * int(item['star_avg'])) / count
    return total_grade


def sort(list,low,high):
    left = low
    right = high
    i = list[low]
    k = count_grate(list[low])
    while left < right:
        while count_grate(list[left]) <= k and left < high:
            left += 1
        while count_grate(list[right]) > k and right > low:
            right -= 1
        if left < right:
            list[left],list[right] = list[right],list[left]
    list[low] = list[right]
    list[right] = i
    return right







