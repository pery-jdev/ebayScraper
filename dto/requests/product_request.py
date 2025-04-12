
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductRequest(BaseModel):
    handle: Optional[str] = Field(None, alias="Product Handle")
    title: Optional[str] = Field(None, alias="Product Title")
    body_html: Optional[str] = Field(None, alias="Body (HTML)")
    vendor: Optional[str] = Field(None, alias="Vendor or Brand Name")
    product_category: Optional[str] = Field(None, alias="Product Category")
    type: Optional[str] = Field(None, alias="Product Type")
    tags: Optional[str] = Field(None, alias="Product Tags")
    published: Optional[bool] = Field(None, alias="Product Status Draft or Published")

    option1_name: Optional[str] = Field(None, alias="Option1 Name")
    option1_value: Optional[str] = Field(None, alias="Option1 Value")
    option1_linked_to: Optional[str] = Field(None, alias="Option1 Linked To")

    option2_name: Optional[str] = Field(None, alias="Option2 Name")
    option2_value: Optional[str] = Field(None, alias="Option2 Value")
    option2_linked_to: Optional[str] = Field(None, alias="Option2 Linked To")

    option3_name: Optional[str] = Field(None, alias="Option3 Name")
    option3_value: Optional[str] = Field(None, alias="Option3 Value")
    option3_linked_to: Optional[str] = Field(None, alias="Option3 Linked To")

    variant_sku: Optional[str] = Field(None, alias="Variant SKU")
    variant_grams: Optional[float] = Field(None, alias="Variant Grams")
    variant_inventory_tracker: Optional[str] = Field(None, alias="Variant Inventory Tracker")
    variant_inventory_policy: Optional[str] = Field(None, alias="Variant Inventory Policy")
    variant_fulfillment_service: Optional[str] = Field(None, alias="Variant Fulfillment Service")
    variant_price: Optional[List[str]] = Field(None, alias="Variant Price")
    variant_compare_at_price: Optional[float] = Field(None, alias="Variant Compare At Price")
    variant_requires_shipping: Optional[bool] = Field(None, alias="Variant Requires Shipping")
    variant_taxable: Optional[bool] = Field(None, alias="Variant Taxable")
    variant_barcode: Optional[str] = Field(None, alias="Variant Barcode")

    image_src: Optional[str] = Field(None, alias="Image Src")
    image_position: Optional[int] = Field(None, alias="Image Position")
    image_alt_text: Optional[str] = Field(None, alias="Image Alt Text")
    gift_card: Optional[bool] = Field(None, alias="Gift Card")

    seo_title: Optional[str] = Field(None, alias="SEO Title")
    seo_description: Optional[str] = Field(None, alias="SEO Description")

    google_product_category: Optional[str] = Field(None, alias="Google Shopping / Google Product Category")
    google_gender: Optional[str] = Field(None, alias="Google Shopping / Gender")
    google_age_group: Optional[str] = Field(None, alias="Google Shopping / Age Group")
    google_mpn: Optional[str] = Field(None, alias="Google Shopping / MPN")
    google_condition: Optional[str] = Field(None, alias="Google Shopping / Condition")
    google_custom_product: Optional[bool] = Field(None, alias="Google Shopping / Custom Product")
    google_custom_label_0: Optional[str] = Field(None, alias="Google Shopping / Custom Label 0")
    google_custom_label_1: Optional[str] = Field(None, alias="Google Shopping / Custom Label 1")
    google_custom_label_2: Optional[str] = Field(None, alias="Google Shopping / Custom Label 2")
    google_custom_label_3: Optional[str] = Field(None, alias="Google Shopping / Custom Label 3")
    google_custom_label_4: Optional[str] = Field(None, alias="Google Shopping / Custom Label 4")

    variant_image: Optional[List[str]] = Field(None, alias="Variant Image")
    variant_weight_unit: Optional[str] = Field(None, alias="Variant Weight Unit")
    variant_tax_code: Optional[str] = Field(None, alias="Variant Tax Code")
    cost_per_item: Optional[float] = Field(None, alias="Cost per item")

    included_japan: Optional[bool] = Field(None, alias="Included / Japan")
    price_japan: Optional[float] = Field(None, alias="Price / Japan")
    compare_at_price_japan: Optional[float] = Field(None, alias="Compare At Price / Japan")

    included_international: Optional[bool] = Field(None, alias="Included / International")
    price_international: Optional[float] = Field(None, alias="Price / International")
    compare_at_price_international: Optional[float] = Field(None, alias="Compare At Price / International")
   

    status: Optional[str]

class Config:
    extra = 'ignore' 
    allow_population_by_field_name = True