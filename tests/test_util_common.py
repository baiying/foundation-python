from src.foundation_python.util.common import short_uuid, load_config, config_value

def test_short_uuid():
    result = short_uuid()
    assert isinstance(result, str)

def test_load_config():
    config_file = '/Users/evan/Code/foundation-python/tests/.config.yml'
    result = load_config(config_file)
    assert result['region'] == 'us'

def test_config_value():
    config_file = '/Users/evan/Code/foundation-python/tests/.config.yml'
    config = load_config(config_file)
    assert config_value(config, 'region') == 'us'
    assert config_value(config, 'log.level') == 'INFO'
    assert config_value(config, 'log.type', 'error') == 'error'

