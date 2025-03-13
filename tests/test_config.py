import os
from core.config import config

def test_config_loading(test_config):
    assert test_config.DEBUG == True
    assert str(test_config.DATA_DIR).endswith('tests/data')
    assert test_config.TRANSLATION['providers']['google']['enabled'] == True
    assert test_config.TRANSLATION['providers']['bing']['enabled'] == False

def test_config_get_method(test_config):
    assert test_config.get('base.debug') == True
    assert test_config.get('translation.providers.google.api_key') == 'TEST_GOOGLE_API_KEY'
    assert test_config.get('non.existent.key', 'default') == 'default'