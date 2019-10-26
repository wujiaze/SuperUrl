# 对数据列表根据星级下载数进行排序
# 1下载数等于3.5星



def sort(data_list):
    data_list = [{'name':'aaa',
                  'download_count':0,
                  'star_one':0,
                  'star_two':0,
                  'star_three':0,
                  'star_four':0,
                  'star_five':0,
                  'star_avg':0,
                  'url':'iii'},
                 {'name': 'aaa',
                  'download_count': 0,
                  'star_one': 0,
                  'star_two': 0,
                  'star_three': 0,
                  'star_four': 0,
                  'star_five': 0,
                  'star_avg': 0,
                  'url': 'iii'},
                 ]

    for item in data_list:
        grade = count_grate(item)




def count_grate(item):
    downloads = int(item['download_count'])
    stars = int(item['star_one'])+ int(item['star_two']) + int(item['star_three']) + int(item['star_four']) + int(item['star_five'])
    count = downloads + stars
    if count == 0:
        return 0
    total_grade = (downloads * 3.5 + stars * int(item['star_avg'])) / count
    return total_grade
