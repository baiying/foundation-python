"""
通用工具
"""
import shortuuid
import os
import yaml
import sys


def short_uuid():
    """
    生成短UUID
    :return:
    """
    return shortuuid.uuid()


def load_global_config():
    """
    加载全局配置
    :return:
    """
    current_dir = os.path.dirname(__file__)
    global_config_file = os.path.abspath(os.path.join(current_dir, '..', 'global_config.yaml'))
    with open(global_config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_local_config():
    """
    加载本地配置
    :return:
    """
    print(f"sys.path: {sys.path[0]}")

