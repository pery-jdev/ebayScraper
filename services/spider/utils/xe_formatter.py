import re

from decimal import Decimal


class XeFormatter(object):
    def __init__(self):
        self.CURRENCY_PATTERN = r"[A-Z]{3}"

    
    def extract_currency_pairs(self, text: str) -> dict:
        patterns = [
            # Format: 1 USD = 148.773 JPY
            re.compile(rf"1\s*({self.CURRENCY_PATTERN})\s*=\s*(\d+\.\d+)\s*({self.CURRENCY_PATTERN})"),
            # Format: 148.773 JPY = 1 USD
            re.compile(rf"(\d+\.\d+)\s*({self.CURRENCY_PATTERN})\s*=\s*1\s*({self.CURRENCY_PATTERN})")
        ]
        
        rates = {}
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    if '1' in groups[0]:  # Format pertama
                        src, rate, dst = groups[0], groups[1], groups[2]
                    else:  # Format kedua
                        rate, dst, src = groups
                    rates[f"{src}_TO_{dst}"] = float(rate)
        
        return rates
    
    # Helper function untuk ekstraksi nilai
    def extract_value(self, text: str) -> Decimal:
        return Decimal(re.sub(r'[^\d.]', '', text))
    
    def eextract_currency(self, text: str) -> str:
        # Mencari kode mata uang 3 huruf yang berdiri sendiri
        match = re.search(r'\b([A-Z]{3})\b(?!.*\b[A-Z]{3}\b)', text)
        if not match:
            raise Exception(f"Tidak ditemukan kode mata uang yang valid dalam teks: {text}")
        return match.group(1)