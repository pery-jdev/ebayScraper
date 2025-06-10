from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Product:
    """Represents a product with its pricing information."""
    title: str
    price_usd: float
    price_aud: float
    id: str = None

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', self.title)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.id == other.id


@dataclass
class Bundle:
    """Represents a bundle of products."""
    id: str
    products: List[Product]
    total_value_usd: float
    total_value_aud: float

    def __post_init__(self):
        # Calculate total values if not provided
        if self.total_value_usd is None:
            self.total_value_usd = sum(p.price_usd for p in self.products)
        if self.total_value_aud is None:
            self.total_value_aud = sum(p.price_aud for p in self.products) 