import os
from dotenv import load_dotenv


def load_setting():
    load_dotenv()
    region = os.getenv('REGION', '')
    if region == '':
        raise Exception("未配置当前区域标识，请配置区域标识后再启动程序")

    local_host = os.getenv('LOCAL_REDIS_HOST', 'localhost')
    local_port = int(os.getenv('LOCAL_REDIS_PORT', '6379'))
    local_db = int(os.getenv('LOCAL_REDIS_HOST', '1'))



