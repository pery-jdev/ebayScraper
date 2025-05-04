import datetime
from decimal import Decimal
from typing import Literal
from dataclasses import dataclass, field

@dataclass
class ConversionMetadataSDC:
    """Metadata for currency conversion process containing technical details
    
    Attributes:
        method: Data retrieval method ('web_scraping' or 'api')
        currency_pair: Currency pair in ISO 4217 format (e.g. USD_JPY)
    """
    method: Literal['web_scraping', 'api'] = field(
        default='web_scraping',
        metadata={"description": "Data retrieval method: 'web_scraping' or 'api'"}
    )
    currency_pair: str = field(
        default=None,
        metadata={
            "pattern": r'^[A-Z]{3}_[A-Z]{3}$',
            "example": 'USD_JPY',
            "description": "Source and target currency pair separated by underscore"
        }
    )


@dataclass
class CurrencyResponseSDC:
    """Currency conversion response containing:
    - Base exchange rate
    - Conversion result
    - Process metadata
    - Conversion timestamp
    """
    source: str = field(
        default='xe.com',
        metadata={"description": "Conversion data source (fixed value)"}
    )
    base_rate: float = field(
        default=None,
        metadata={"description": "Exchange rate per 1 unit of source currency"}
    )
    result: float = field(
        default=None,
        metadata={"description": "Final conversion result in target currency"}
    )
    metadata: ConversionMetadataSDC = field(default=None)
    timestamp: datetime.datetime = field(
        default_factory=datetime.datetime.utcnow,
        metadata={"description": "Conversion execution time in UTC"}
    )
