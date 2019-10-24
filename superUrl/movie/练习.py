import redis


r=redis.Redis('127.0.0.1',6379,db=1)
a=r.lrange('gao',0,-1)
print(a)
for i in a:
    i=i.decode()
    print(type(i))

b=r.lrange('liu',0,-1)
print(b)
for n in b:
    n=n.decode()
    print(n)