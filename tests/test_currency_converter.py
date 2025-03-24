# tests/pricing/test_currency_converter.py
import pytest
from unittest.mock import patch
from services.pricing.alphavantage_converter import AlphaVantageConverter
from services.pricing.currency_converter import CurrencyConverter
from services.spider.xe import XeSpider

@pytest.fixture
def converter():
    return CurrencyConverter()

def test_successful_alpha_vantage(converter):
    with patch('services.pricing.alphavantage_converter.AlphaVantageConverter.get_rates') as mock_av:
        mock_av.return_value = 150.0
        assert converter.get_rate("USD", "JPY") == 150.0
        mock_av.assert_called_once_with("USD", "JPY")

def test_fallback_to_xe(converter):
    with patch('services.pricing.alphavantage_converter.AlphaVantageConverter.get_rates') as mock_av, \
         patch('services.spider.xe.XeSpider.scrape_rate') as mock_xe:
        
        mock_av.side_effect = ConnectionError("API rate limit exceeded")
        mock_xe.return_value = 148.5
        
        result = converter.get_rate("USD", "JPY")
        assert result == 148.5
        assert mock_av.call_count == 3  # 3 retries
        mock_xe.assert_called_once_with("USD", "JPY")

def test_all_providers_fail(converter):
    with patch('services.pricing.alphavantage_converter.AlphaVantageConverter.get_rates') as mock_av, \
         patch('services.spider.xe.XeSpider.scrape_rate') as mock_xe:
        
        mock_av.side_effect = ConnectionError("API rate limit exceeded")
        mock_xe.side_effect = Exception("XE failed")
        
        with pytest.raises(ValueError):
            converter.get_rate("USD", "JPY")

def test_config_loading():
    with patch('core.config.config.get') as mock_config:
        mock_config.return_value = {
            'max_retries': 5,
            'retry_delay': 1
        }
        
        converter = CurrencyConverter()
        assert converter.retry_count == 5
        assert converter.retry_delay == 1

def test_xe_decimal_precision():
    spider = XeSpider()
    
    # Test case 1: Nilai bulat
    result = spider.scrape_rate(1000, "USD", "JPY")
    assert round(result['converted_amount'], 2) == result['converted_amount']
    
    # Test case 2: Nilai pecahan kompleks
    result = spider.scrape_rate(1234.56, "AUD", "USD")
    aud_usd_rate = result['calculation_steps']['rate_used']
    assert len(str(aud_usd_rate).split('.')[1]) <= 6  # Presisi 6 digit
    
    # Test case 3: Perbandingan dengan AlphaVantage
    av_result = AlphaVantageConverter().get_rates("AUD", "USD", 1)
    assert abs(result['converted_amount'] - av_result['converted_amount']) < 0.02