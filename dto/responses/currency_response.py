import datetime

from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ConversionMetadata(BaseModel):
    """Metadata for currency conversion process containing technical details
    
    Attributes:
        method: Data retrieval method ('web_scraping' or 'api')
        currency_pair: Currency pair in ISO 4217 format (e.g. USD_JPY)
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    method: Literal['web_scraping', 'api'] = Field(
        default='web_scraping',
        description="Data retrieval method: 'web_scraping' or 'api'"
    )
    currency_pair: str = Field(
        ...,
        pattern=r'^[A-Z]{3}_[A-Z]{3}$',
        example='USD_JPY',
        description="Source and target currency pair separated by underscore"
    )


class CurrencyResponse(BaseModel):
    """Currency conversion response containing:
    - Base exchange rate
    - Conversion result
    - Process metadata
    - Conversion timestamp
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    source: str = Field(
        default='xe.com',
        description="Conversion data source (fixed value)"
    )
    base_rate: float = Field(
        ...,
        gt=0,
        description="Exchange rate per 1 unit of source currency"
    )
    result: float = Field(
        ...,
        description="Final conversion result in target currency"
    )
    metadata: ConversionMetadata
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        description="Conversion execution time in UTC"
    )

    @field_validator('base_rate')
    def validate_rate_precision(cls, v):
        """Round exchange rate to 6 decimal places"""
        return round(v, 6)

    @classmethod
    @classmethod
    def from_conversion(
        cls,
        amount: Decimal,
        rate: Decimal,
        currency_pair: str,
        method: Literal['web_scraping', 'api'],
        source: str  # Added source parameter
    ) -> 'CurrencyResponse':
        return cls(
            source=source,
            base_rate=float(rate.quantize(Decimal('0.000001'))),
            result=float((amount * rate).quantize(Decimal('0.00'))),
            metadata=ConversionMetadata(
                method=method,
                currency_pair=currency_pair.upper()
            )
        )