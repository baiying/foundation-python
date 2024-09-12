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
    project_root = sys.path[0]
    local_config_file = os.path.abspath(os.path.join(project_root, 'local_config.yaml'))
    if not os.path.exists(local_config_file):
        raise FileNotFoundError('未找到本地配置文件 local_config.yaml，请创建该配置文件后再次尝试')
    with open(local_config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_config():
    """
    加载全局配置和本地配置
    :return:
    """
    global_config = load_global_config()
    local_config = load_local_config()
    return {**global_config, **local_config}



