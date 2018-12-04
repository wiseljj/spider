import redis
from . import BaseFilter
#利用redis去重
class RedisFilter(BaseFilter):
    def _get_storage(self):
        #建立连接池
        pool=redis.ConnectionPool(host=self.redis_host,port=self.redis_port,db=self.redis_db)
        client=redis.StrictRedis(connection_pool=pool)
        return client

    def _save(self,hash_value):
        return self.storage.sadd(self.redis_key,hash_value)

    def _is_exists(self,hash_value):
        return self.storage.sismember(self.redis_key,hash_value)
