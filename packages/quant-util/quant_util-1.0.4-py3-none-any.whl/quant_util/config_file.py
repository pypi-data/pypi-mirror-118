import os
import warnings

# tushare token
db_data_start = "2015-01-01"
tushare_token = os.getenv('tushare_token')
if tushare_token is None:
    tushare_token = ''
    warnings.warn('tushare token is None!')
else:
    print(f'tushare token is {tushare_token}')


# clickhouse connection
clickhouse_host = os.getenv('clickhouse_host')
if clickhouse_host is None:
    clickhouse_host = 'localhost'
print(f'clickhouse_host is {clickhouse_host}')
clickhouse_db_name = "quant"
pandahouse_connection_dict = {'host': f'http://{clickhouse_host}:8123',
                              'database': clickhouse_db_name}

# mongo host
mongo_api_host = os.getenv("db_api_host")
if not mongo_api_host:
    mongo_api_host = "localhost"
print("mongo_api_host", mongo_api_host)

# rabbitmq_host
rabbitmq_host = os.getenv("rabbitmq_host")
if not rabbitmq_host:
    rabbitmq_host = "localhost"
print("rabbitmq_host", rabbitmq_host)

# redis_host
redis_host = os.getenv("redis_host")
if not redis_host:
    redis_host = "localhost"
print("redis_host", redis_host)

