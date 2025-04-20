import logging
from typing import Dict
from services.pricing.currency_converter import CurrencyConverter

class CurrencyManager:
    def __init__(self):
        self.converter = CurrencyConverter()
        self.logger = logging.getLogger(__name__)
        self.target_currencies = ["USD", "EUR", "AUD"]  # Default target currencies

    def calculate_price_map(self, base_currency: str, base_amount: float) -> Dict[str, float]:
        """Calculate prices in all target currencies
        
        Args:
            base_currency: Original currency code (e.g. "JPY")
            base_amount: Original price amount
            
        Returns:
            Dictionary of {currency: converted_price}
        """
        price_map = {}
        
        try:
            for currency in self.target_currencies:
                if currency == base_currency:
                    price_map[currency] = base_amount
                else:
                    converted = self.converter.convert_currency(
                        base_currency,
                        currency,
                        base_amount
                    )
                    price_map[currency] = converted
                    
        except Exception as e:
            self.logger.error(f"Failed to calculate prices: {str(e)}")
            price_map = {base_currency: base_amount}  # Fallback to base currency
            
        return price_map

    def set_target_currencies(self, currencies: list):
        """Update the target currencies for price calculation"""
        self.target_currencies = currencies
