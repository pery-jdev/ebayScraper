
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductRequest(BaseModel):
    handle: str = Field(..., description="Unique identifier for the product")
    title: Optional[str] = Field(None, description="Product title")
    vendor: Optional[str] = Field(None, description="Vendor or brand of the product")
    type: Optional[str] = Field(None, description="Type or category of the product")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    published: Optional[bool] = Field(None, description="Whether the product is published")
    option1_name: Optional[str] = Field(None, description="First option name (e.g., Color, Size)")
    option1_value: Optional[str] = Field(None, description="Value of the first option")
    variant_price: Optional[List[float]] = Field(None, description="Price of the product variant")
    variant_inventory_tracker: Optional[str] = Field(None, description="Inventory tracking method")
    variant_grams: Optional[float] = Field(None, description="Weight of the product in grams")
    variant_requires_shipping: Optional[bool] = Field(None, description="Does the product require shipping")
    variant_taxable: Optional[bool] = Field(None, description="Is the product taxable")
    image_src: Optional[List[str]] = Field(default_factory=list, description="List of product image URLs")
    variant_image: Optional[List[str]] = Field(default_factory=list, description="List of variant image URLs")
    status: Optional[str] = Field(None, description="Current status of the product")
