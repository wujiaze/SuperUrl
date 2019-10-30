import json

import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=1)

r.set('music:keylist:a', '["a","b"]')
r.set('music:keylist:ab', '["周杰伦","你好"]')
r.set('music:keylist:b', '["我和你","同住地球村"]')

r.set('movie:keylist:a', '["a","b"]')
r.set('movie:keylist:b', '["我和你","同住地球村"]')

r.set('picture:keylist:a', '["a","b"]')
r.set('picture:keylist:b', '["我和你","同住地球村"]')

data = [
    {
        "url": "www.baidu.com",
        "name": "彩虹",
        "star": "周杰伦",
        "star_one": "1",
        "star_two": "2",
        "star_three": "3",
        "star_four": "4",
        "star_five": "5",
        "download_count": "10",
        "star_avg": "4"
    },
    {
        "url": "www.baidu.com",
        "name": "彩虹",
        "star": "周杰伦",
        "star_one": "1",
        "star_two": "2",
        "star_three": "3",
        "star_four": "4",
        "star_five": "5",
        "download_count": "10",
        "star_avg": "4"
    }
]

r.set('music:new', json.dumps(data))
r.set('music:hot', json.dumps(data))

data = []
for i in range(200):
    index_pic = str(i % 12 + 1)
    hre = "/static/image/images/image" + index_pic + ".jpg"
    data.append({
        "url": hre,
        "describe": "彩虹",
        "download_count": "1",
    })
r.set('picture:search',json.dumps(data))
# r.set('info:picture:美图', json.dumps(data))

print('成功')
