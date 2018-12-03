from info_filter.redis_filter import RedisFilter
filter=RedisFilter()


data=["333","4","444","333","dd","s","dd"]
for i in data:
    if filter.is_exists(i):
        print("重复")
    else:
        filter.save(i)
        print('已经保存')