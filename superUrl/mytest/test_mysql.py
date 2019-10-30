import hashlib
import random

import redis

from index.models import Finger
from music.models import MusicKeyword, MusicInformation

r = redis.Redis(db=1)





# 模拟爬虫 定时更新,获取新歌，放入mysql，建立关联，放入redis，将热歌从信息库中放入redis

# redis 中 新歌，热歌，搜索结果 的 存储形式 和返回形式

