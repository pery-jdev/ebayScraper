# scraping for xe.com to generate currency rates data
import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Dict
import pandas as pd

from services.spider.errors.xe import XEScrapingError
from services.spider.response import XeResponse
from services.spider.parser import XeParser


class XeSpider:
    def __init__(self):
        self.response: XeResponse = XeResponse()
        self.parser: XeParser = XeParser()


    def scrape_rate(self, ammount: int, from_curr: str, to_curr: str):
        url = f"https://www.xe.com/en/currencyconverter/convert/?Amount={ammount}&From={from_curr}&To={to_curr}"
        response = self.response.get_response(url=url)
        rates = self.parser.parse_rate(response)
        return rates

    def get_conversion_rate(self, amount: int, from_curr: str, to_curr: str) -> Dict:
        """Main interface untuk mendapatkan rate konversi"""
        try:
            url = self._build_url(amount, from_curr, to_curr)
            html = self.response.get_response(url)
            raw_rate = self.parser.parse_rates(html)
            return self._format_response(raw_rate, amount, from_curr, to_curr)
        except Exception as e:
            error_msg = f"XE Scraping failed: {str(e)}"
            raise XEScrapingError(error_msg) from e

    def _build_url(self, amount: int, from_curr: str, to_curr: str) -> str:
        """Membangun URL untuk scraping"""
        return f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_curr}&To={to_curr}"

    def _format_response(self, rate: float, amount: int, from_curr: str, to_curr: str) -> Dict:
        """Membentuk response sesuai standar sistem"""
        decimal_rate = Decimal(str(rate)).quantize(Decimal('0.000000'), rounding=ROUND_HALF_UP)
        converted = (Decimal(amount) * decimal_rate).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        
        return {
            "source": "xe.com",
            "base_rate": float(decimal_rate),
            "calculated_rate": float(decimal_rate),
            "converted_amount": float(converted),
            "metadata": {
                "method": "web_scraping",
                "currencies": f"{from_curr}_{to_curr}"
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }