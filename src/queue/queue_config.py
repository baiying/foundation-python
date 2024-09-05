import os
from dotenv import load_dotenv

load_dotenv()
# 加载当前区域标识
REGION = os.getenv('REGION', '')
if REGION == '':
    print("未配置当前区域标识，请配置区域标识后再启动程序")
    exit(1)

# 加载中心REDIS配置
CENTRAL_REDIS_HOST = os.getenv('CENTRAL_REDIS_HOST', 'localhost')
CENTRAL_REDIS_PORT = int(os.getenv('CENTRAL_REDIS_PORT', 6379))
CENTRAL_REDIS_DB = int(os.getenv('CENTRAL_REDIS_DB', 0))
# 连接失败重新尝试次数
CONNECT_FAILED_RETRY = int(os.getenv('CONNECT_FAILED_RETRY'), 3)
# 消息队列前缀
QUEUE_PREFIX = os.getenv('QUEUE_PREFIX', 'cv')

