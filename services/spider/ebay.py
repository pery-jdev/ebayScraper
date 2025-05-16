import json
import re
from typing import Any
from bs4 import BeautifulSoup


from services.spider.parser import EbayParser
from services.spider.response import SpiderResponse
from core.config import config as cfg

from dto.requests.product_request_sdc import ProductRequestSDC as ProductRequest


class EbaySpider(object):
    def __init__(self):
        self.base_url: list[str] = ["https://www.ebay.com.au/", "https://www.ebay.com"]
        self.response: SpiderResponse = SpiderResponse()
        self.parser: EbayParser = EbayParser()

    def get_products(self, query: str):
        product_lists: list[ProductRequest] = []
        response = self.response.get_response(
            url=f"{self.base_url[0]}sch/i.html?",
            params={
                "_nkw": query,
                "_sacat": 0,
                "_from": "R40",
                "_trksid": "p2334524.m570.l1313",
                "_odkw": "laptop",
                "_osacat": 0,
            },
            mode="selenium",
        )

        products = self.parser.parse_products(soup=response)

        for product in products:
            product_url = product['product_url']
            product_details = self.get_product_details(product_url)

            # Extract price and remove non-numeric characters
            price_string = product_details.prices.price_primary if product_details.prices else None
            variant_price = float(re.sub(r"[^0-9.]", "", price_string)) if price_string else None

            mapped_product = ProductRequest(
                handle=getattr(product, 'handle', None),
                title=getattr(product, 'title', None),
                body_html=product_details.body_html,
                vendor=product_details.vendor,
                product_category=product_details.product_category,
                variant_sku=product_details.variant_sku,
                image_src=product_details.image_src,
                image_alt_text=product_details.image_alt_text,
                variant_price=variant_price,
                # Condition=product_details.Condition,
                # Brand=product_details.Brand,
                # Bait_Type=product_details.Bait_Type,
                # Bait_Shape=getattr(product_details, 'Bait_Shape', None), # Assuming Bait_Shape might be missing
                # Buoyancy=getattr(product_details, 'Buoyancy', None), # Assuming Buoyancy might be missing
                # Number_in_Pack=getattr(product_details, 'Number_in_Pack', None), # Assuming Number_in_Pack might be missing
                # Material=getattr(product_details, 'Material', None), # Assuming Material might be missing
                # Item_Weight=getattr(product_details, 'Item_Weight', None), # Assuming Item_Weight might be missing
                # Colour=getattr(product_details, 'Colour', None) # Assuming Colour might be missing
            )
            product_lists.append(mapped_product)

        return product_lists

    def get_product_details(self, url: str):
        response = self.response.get_response(url=url, mode="selenium")
        # f = open(cfg.TEMP_DIR / "response.html", "r")
        # soup = BeautifulSoup(f.read(), "html.parser")
        product = self.parser.parse_product_details(soup=response)
        return product

    def generate_products(self, query: str, category: str = None):
        products = self.get_products(query=query)
        print(products)
        return products

        # Format produk sesuai kebutuhan API

    def format_products(self, products: list[Any]):
        formatted_products = []
        for product in products:
            product_data = {
                "handle": product.get("handle"),
                "title": product.get("title"),
                "body_html": product.get("body_html"),
                "vendor": product.get("vendor"),
                "product_category": product.get("product_category"),
                "type": product.get("type"),
                "tags": product.get("tags"),
                "published": product.get("published"),
                "option1_name": product.get("option1_name"),
                "option1_value": product.get("option1_value"),
                "option1_linked_to": product.get("option1_linked_to"),
                "option2_name": product.get("option2_name"),
                "option2_value": product.get("option2_value"),
                "option2_linked_to": product.get("option2_linked_to"),
                "option3_name": product.get("option3_name"),
                "option3_value": product.get("option3_value"),
                "option3_linked_to": product.get("option3_linked_to"),
                "variant_sku": product.get("variant_sku"),
                "variant_grams": product.get("variant_grams"),
                "variant_inventory_tracker": product.get(
                    "variant_inventory_tracker"
                ),
                "variant_inventory_qty": product.get("variant_inventory_qty"),
                "variant_inventory_policy": product.get(
                    "variant_inventory_policy"
                ),
                "variant_fulfillment_service": product.get(
                    "variant_fulfillment_service"
                ),
                "variant_price": product.get("variant_price"),
                "variant_compare_at_price": product.get(
                    "variant_compare_at_price"
                ),
                "variant_requires_shipping": product.get(
                    "variant_requires_shipping"
                ),
                "variant_taxable": product.get("variant_taxable"),
                "variant_barcode": product.get("variant_barcode"),
                "image_src": product.get("image_src"),
                "image_position": product.get("image_position"),
                "image_alt_text": product.get("image_alt_text"),
                "gift_card": product.get("gift_card"),
                "seo_title": product.get("seo_title"),
                "seo_description": product.get("seo_description"),
                "google_product_category": product.get(
                    "google_product_category"
                ),
                "google_gender": product.get("google_gender"),
                "google_age_group": product.get("google_age_group"),
                "google_mpn": product.get("google_mpn"),
                "google_adwords_grouping": product.get(
                    "google_adwords_grouping"
                ),
                "google_adwords_labels": product.get("google_adwords_labels"),
                "google_condition": product.get("google_condition"),
                "google_custom_product": product.get("google_custom_product"),
                "google_custom_label_0": product.get("google_custom_label_0"),
                "google_custom_label_1": product.get("google_custom_label_1"),
                "google_custom_label_2": product.get("google_custom_label_2"),
                "google_custom_label_3": product.get("google_custom_label_3"),
                "google_custom_label_4": product.get("google_custom_label_4"),
                "variant_image": product.get("variant_image"),
                "variant_weight_unit": product.get("variant_weight_unit"),
                "variant_tax_code": product.get("variant_tax_code"),
                "cost_per_item": product.get("cost_per_item"),
                "included_japan": product.get("included_japan"),
                "price_japan": product.get("price_japan"),
                "compare_at_price_japan": product.get("compare_at_price_japan"),
                "included_international": product.get("included_international"),
                "price_international": product.get("price_international"),
                "compare_at_price_international": product.get(
                    "compare_at_price_international"
                ),
                "status": product.get("status"),
            }
            formatted_products.append(product_data)

        with open("products.json", "w") as f:
            json.dump(formatted_products, f, indent=4)
        return formatted_products
