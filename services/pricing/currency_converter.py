from decimal import Decimal
import logging
import time
from typing import Optional
from dto.responses.currency_response import CurrencyResponse
from services.pricing.alphavantage_converter import AlphaVantageConverter
from services.spider.xe import XeSpider


class CurrencyConverter(object):
    def __init__(self):
        self.av = AlphaVantageConverter()
        self.xe = XeSpider()
        self.retry_count = 3
        self.retry_delay = 2  # detik
        
    def get_rate(self, from_curr="USD", to_curr="JPY"):
        for attempt in range(self.retry_count):
            try:
                # Coba AlphaVantage pertama
                rates = self.av.get_rates()
                return rates[f"{from_curr}_{to_curr}"]
            except Exception as e:
                if attempt == self.retry_count - 1:
                    logging.warning("AlphaVantage limit exceeded, falling back to XE")
                    return self._fallback_to_xe(from_curr, to_curr)
                logging.info(f"Retrying AlphaVantage ({attempt+1}/{self.retry_count})")
                time.sleep(self.retry_delay * (attempt + 1))
                
        return self._fallback_to_xe(from_curr, to_curr)
        
    def _fallback_to_xe(self,  from_curr, to_curr):
        try:
            return self.xe.scrape_rate(from_curr, to_curr)
        except Exception as e:
            logging.error("XE fallback failed")
            raise ValueError("All conversion methods failed") from e

    def convert_currency(self, from_curr: str, to_curr: str, amount: float, method: Optional[str]=None) -> CurrencyResponse:
        if method == None:
            try:
                # Try API first
                return self.av.get_rates(from_curr, to_curr, amount)
            except Exception as api_error:
                # Fallback to web scraping
                xe_rate = self.xe.scrape_rate(from_curr=from_curr, to_curr=to_curr, ammount=amount)
                return CurrencyResponse.from_conversion(
                    amount=Decimal(str(amount)),
                    rate=xe_rate,
                    currency_pair=f"{from_curr}_{to_curr}",
                    method='web_scraping',
                    source='xe.com'
                )
        elif method == 'api':
            return self.av.get_rates(from_curr, to_curr, amount)
        elif method == 'web_scraping':
            return self.xe.scrape_rate(from_curr, to_curr, amount)
        else:
            raise ValueError("Invalid method")