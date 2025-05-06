from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ProductRequestSDC:
    handle: Optional[str] = field(default=None, metadata={"alias": "Handle"})
    title: Optional[str] = field(default=None, metadata={"alias": "Title"})
    body_html: Optional[str] = field(default=None, metadata={"alias": "Body (HTML)"})
    vendor: Optional[str] = field(default=None, metadata={"alias": "Vendor"})
    product_category: Optional[str] = field(default=None, metadata={"alias": "Product Category"})
    type: Optional[str] = field(default=None, metadata={"alias": "Type"})
    tags: Optional[str] = field(default=None, metadata={"alias": "Tags"})
    published: Optional[str] = field(default=None, metadata={"alias": "Published"})

    option1_name: Optional[str] = field(default=None, metadata={"alias": "Option1 Name"})
    option1_value: Optional[str] = field(default=None, metadata={"alias": "Option1 Value"})
    option1_linked_to: Optional[str] = field(default=None, metadata={"alias": "Option1 Linked To"})
    option2_name: Optional[str] = field(default=None, metadata={"alias": "Option2 Name"})
    option2_value: Optional[str] = field(default=None, metadata={"alias": "Option2 Value"})
    option2_linked_to: Optional[str] = field(default=None, metadata={"alias": "Option2 Linked To"})
    option3_name: Optional[str] = field(default=None, metadata={"alias": "Option3 Name"})
    option3_value: Optional[str] = field(default=None, metadata={"alias": "Option3 Value"})
    option3_linked_to: Optional[str] = field(default=None, metadata={"alias": "Option3 Linked To"})

    variant_sku: Optional[str] = field(default=None, metadata={"alias": "Variant SKU"})
    variant_grams: Optional[float] = field(default=None, metadata={"alias": "Variant Grams"})
    variant_inventory_tracker: Optional[str] = field(default=None, metadata={"alias": "Variant Inventory Tracker"})
    variant_inventory_qty: Optional[int] = field(default=None, metadata={"alias": "Variant Inventory Qty"})
    variant_inventory_policy: Optional[str] = field(default=None, metadata={"alias": "Variant Inventory Policy"})
    variant_fulfillment_service: Optional[str] = field(default=None, metadata={"alias": "Variant Fulfillment Service"})
    variant_price: Optional[float] = field(default=None, metadata={"alias": "Variant Price"})
    variant_compare_at_price: Optional[float] = field(default=None, metadata={"alias": "Variant Compare At Price"})
    variant_requires_shipping: Optional[bool] = field(default=None, metadata={"alias": "Variant Requires Shipping"})
    variant_taxable: Optional[bool] = field(default=None, metadata={"alias": "Variant Taxable"})
    variant_barcode: Optional[str] = field(default=None, metadata={"alias": "Variant Barcode"})

    image_src: Optional[str] = field(default=None, metadata={"alias": "Image Src"})
    image_position: Optional[int] = field(default=None, metadata={"alias": "Image Position"})
    image_alt_text: Optional[str] = field(default=None, metadata={"alias": "Image Alt Text"})

    gift_card: Optional[bool] = field(default=None, metadata={"alias": "Gift Card"})
    seo_title: Optional[str] = field(default=None, metadata={"alias": "SEO Title"})
    seo_description: Optional[str] = field(default=None, metadata={"alias": "SEO Description"})

    google_product_category: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Google Product Category"})
    google_gender: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Gender"})
    google_age_group: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Age Group"})
    google_mpn: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / MPN"})
    google_adwords_grouping: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Adwords Grouping"})
    google_adwords_labels: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Adwords Labels"})
    google_condition: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Condition"})
    google_custom_product: Optional[bool] = field(default=None, metadata={"alias": "Google Shopping / Custom Product"})
    google_custom_label_0: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Custom Label 0"})
    google_custom_label_1: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Custom Label 1"})
    google_custom_label_2: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Custom Label 2"})
    google_custom_label_3: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Custom Label 3"})
    google_custom_label_4: Optional[str] = field(default=None, metadata={"alias": "Google Shopping / Custom Label 4"})

    variant_image: Optional[str] = field(default=None, metadata={"alias": "Variant Image"})
    variant_weight_unit: Optional[str] = field(default=None, metadata={"alias": "Variant Weight Unit"})
    variant_tax_code: Optional[str] = field(default=None, metadata={"alias": "Variant Tax Code"})
    cost_per_item: Optional[float] = field(default=None, metadata={"alias": "Cost per item"})

    included_japan: Optional[bool] = field(default=None, metadata={"alias": "Included / Japan"})
    price_japan: Optional[float] = field(default=None, metadata={"alias": "Price / Japan"})
    compare_at_price_japan: Optional[float] = field(default=None, metadata={"alias": "Compare At Price / Japan"})

    included_international: Optional[bool] = field(default=None, metadata={"alias": "Included / International"})
    price_international: Optional[float] = field(default=None, metadata={"alias": "Price / International"})
    compare_at_price_international: Optional[float] = field(default=None, metadata={"alias": "Compare At Price / International"})

    status: Optional[str] = field(default=None, metadata={"alias": "Status"})



@dataclass
class ProductDetailsRequestSDC:
    body_html: Optional[str] = None
    image_src: Optional[str] = None
    image_alt_text: Optional[str] = None
    vendor: Optional[str] = None
    product_category: Optional[str] = None
    variant_sku: Optional[str] = None
    prices: Optional[dict[str, str]] = field(default_factory=dict)
    Condition: Optional[str] = None
    Brand: Optional[str] = None
    Bait_Type: Optional[str] = None
    Bait_Shape: Optional[str] = None
    Buoyancy: Optional[str] = None
    Number_in_Pack: Optional[str] = None
    Material: Optional[str] = None
    Item_Weight: Optional[str] = None
    Colour: Optional[str] = None
    # Tambahkan atribut lain sesuai kebutuhan
