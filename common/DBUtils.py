# import psycopg2

# conn = psycopg2.connect(
#     database="Proxy",
#     user="postgres",
#     password="kaba5643",
#     host="192.168.31.148",
#     port="55433",
# )
# print("Opened database successfully")

import json

# cur = conn.cursor()
# cur.execute("SELECT name, threshhold0, threshhold1  from sjy_aqi_threshhold")
# rows = cur.fetchall()
# for row in rows:
#     print("NAME = ")
#     print("threshhold0 = ")
#     print("threshhold0 = ")
# print("Operation done successfully")
# conn.close()
from redis import Redis


class RedisProfile(object):
    host = "192.168.31.148"
    port = 56379


class DBOpration(object):
    def __init__(self) -> None:
        pass


class RedisOpration(DBOpration):
    def __init__(self, profile) -> None:
        super().__init__()
        self.conn = Redis(host=profile.host, port=profile.port)

    def redis_data_2_dict(self, data):
        return json.loads(data.decode("utf-8"))

    def dict_2_redis_data(self, data):
        return json.dumps(data, ensure_ascii=False)

    def sadd(self, key, value):
        if self.conn.sadd(key, value):
            return True
        return False

    def smembers(self, key):
        data_list = self.conn.smembers(key)
        return [self.redis_data_2_dict(data) for data in data_list]

    def srem(self, key, value):
        data = self.dict_2_redis_data(value)
        return self.conn.srem(key, data)

    def scard(self, key):
        return self.conn.scard(key)
