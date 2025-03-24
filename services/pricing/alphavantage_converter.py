import requests
from typing import Dict
from decimal import Decimal
from datetime import datetime
from core.config import config

class AlphaVantageConverter:
    """Handler untuk konversi mata uang menggunakan AlphaVantage API
    
    Fitur:
    - Konversi langsung dan cross-rate via USD
    - Perhitungan jumlah konversi
    - Error handling terstruktur
    - Dokumentasi rate secara detail
    
    Contoh penggunaan:
    >>> converter = AlphaVantageConverter()
    >>> result = converter.get_rates("JPY", "AUD", amount=8000)
    >>> print(result['converted_amount'])
    78.00
    """
    
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = config.ALPHA_VANTAGE_KEY
        self.base_currency = "USD"  # Mata uang dasar untuk cross-rate

    def get_rates(self, from_curr: str="USD", to_curr: str="JPY", amount: float = 1.0) -> Dict:
        """Mendapatkan rate konversi dan jumlah terkonversi
        
        Args:
            from_curr: Kode mata uang asal (3 huruf)
            to_curr: Kode mata uang tujuan (3 huruf)
            amount: Jumlah yang akan dikonversi
            
        Returns:
            Dict berisi:
            - base_rate: Rate langsung dari API
            - calculated_rate: Rate akhir yang digunakan
            - converted_amount: Jumlah terkonversi
            - is_cross_rate: True jika menggunakan cross-rate
            - metadata: Info tambahan tentang sumber rate
        """
        try:
            # Coba dapatkan rate langsung
            direct_rate = self._get_direct_rate(from_curr, to_curr)
            return self._build_response(
                direct_rate, 
                from_curr, 
                to_curr, 
                amount,
                is_cross_rate=False
            )
        except Exception as e:
            # Fallback ke cross-rate via USD
            usd_rate1 = self._get_direct_rate(from_curr, self.base_currency)
            usd_rate2 = self._get_direct_rate(self.base_currency, to_curr)
            calculated_rate = usd_rate1 * usd_rate2
            
            return self._build_response(
                calculated_rate,
                from_curr,
                to_curr,
                amount,
                is_cross_rate=True,
                metadata={
                    'base_currency': self.base_currency,
                    'components': {
                        f"{from_curr}_{self.base_currency}": usd_rate1,
                        f"{self.base_currency}_{to_curr}": usd_rate2
                    }
                }
            )

    def _get_direct_rate(self, from_curr: str, to_curr: str) -> Decimal:
        """Mendapatkan rate langsung dari API"""
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_curr,
            "to_currency": to_curr,
            "apikey": self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        rate_str = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        return Decimal(rate_str)

    def _build_response(self, 
                      rate: Decimal,
                      from_curr: str,
                      to_curr: str,
                      amount: float,
                      is_cross_rate: bool,
                      metadata: Dict = None) -> Dict:
        """Membangun response terstruktur"""
        converted = Decimal(amount) * rate
        
        return {
            "base_rate": float(rate),
            "calculated_rate": float(rate),
            "converted_amount": round(float(converted), 2),
            "is_cross_rate": is_cross_rate,
            "metadata": metadata or {},
            "calculation_steps": {
                "input_amount": amount,
                "from_currency": from_curr,
                "to_currency": to_curr,
                "rate_used": float(rate),
                "timestamp": datetime.utcnow().isoformat(timespec='seconds') + "Z"  # UTC time sesuai ISO 8601
            }
        }
