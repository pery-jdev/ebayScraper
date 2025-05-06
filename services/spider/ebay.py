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
        product_lists: list[dict[str, Any]] = []
        #! kelas ini harsunya untuk menggabungkan parsing product di halamaman search dan detail
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
        # f = open(cfg.TEMP_DIR / "response.html", "r")
        # soup = BeautifulSoup(f.read(), "html.parser")

        products = self.parser.parse_products(soup=response)

        for product in products:
            # process here
            product_url = product["product_url"]
            product_details = self.get_product_details(product_url)
            product_data: ProductRequest = ProductRequest(
                handle=product.get("handle"),
                title=product.get("title"),
                body_html=product_details.body_html,
                vendor=product_details.vendor
            )
            product_lists.append(product_data)

        return product_lists

    def get_product_details(self, url: str):
        # response = self.response.get_response(url=url, mode="selenium")
        f = open(cfg.TEMP_DIR / "response.html", "r")
        soup = BeautifulSoup(f.read(), "html.parser")
        product = self.parser.parse_product_details(soup=soup)
        return product

    def generate_products(self, query: str, category: str = None):
        products = self.get_products(query=query)

        # Format produk sesuai kebutuhan API
        formatted_products = []
        for product in products:
            formatted_products.append(
                {
                    "handle": getattr(product, "handle", ""),
                    "title": getattr(product, "title", ""),
                    "body_html": getattr(product, "body_html", ""),
                    "vendor": getattr(product, "vendor", ""),
                    "product_category": getattr(product, "product_category", ""),
                    "type": getattr(product, "type", ""),
                    "tags": getattr(product, "tags", ""),
                    "published": getattr(product, "published", ""),
                    "option1_name": getattr(product, "option1_name", ""),
                    "option1_value": getattr(product, "option1_value", ""),
                    "option1_linked_to": getattr(product, "option1_linked_to", ""),
                    "option2_name": getattr(product, "option2_name", ""),
                    "option2_value": getattr(product, "option2_value", ""),
                    "option2_linked_to": getattr(product, "option2_linked_to", ""),
                    "option3_name": getattr(product, "option3_name", ""),
                    "option3_value": getattr(product, "option3_value", ""),
                    "option3_linked_to": getattr(product, "option3_linked_to", ""),
                    "variant_sku": getattr(product, "variant_sku", ""),
                    "variant_grams": getattr(product, "variant_grams", 0),
                    "variant_inventory_tracker": getattr(
                        product, "variant_inventory_tracker", ""
                    ),
                    "variant_inventory_qty": getattr(
                        product, "variant_inventory_qty", 0
                    ),
                    "variant_inventory_policy": getattr(
                        product, "variant_inventory_policy", ""
                    ),
                    "variant_fulfillment_service": getattr(
                        product, "variant_fulfillment_service", ""
                    ),
                    "variant_price": getattr(product, "variant_price", 0),
                    "variant_compare_at_price": getattr(
                        product, "variant_compare_at_price", 0
                    ),
                    "variant_requires_shipping": getattr(
                        product, "variant_requires_shipping", False
                    ),
                    "variant_taxable": getattr(product, "variant_taxable", False),
                    "variant_barcode": getattr(product, "variant_barcode", ""),
                    "image_src": getattr(product, "image_src", ""),
                    "image_position": getattr(product, "image_position", 0),
                    "image_alt_text": getattr(product, "image_alt_text", ""),
                    "gift_card": getattr(product, "gift_card", False),
                    "seo_title": getattr(product, "seo_title", ""),
                    "seo_description": getattr(product, "seo_description", ""),
                    "google_product_category": getattr(
                        product, "google_product_category", ""
                    ),
                    "google_gender": getattr(product, "google_gender", ""),
                    "google_age_group": getattr(product, "google_age_group", ""),
                    "google_mpn": getattr(product, "google_mpn", ""),
                    "google_adwords_grouping": getattr(
                        product, "google_adwords_grouping", ""
                    ),
                    "google_adwords_labels": getattr(
                        product, "google_adwords_labels", ""
                    ),
                    "google_condition": getattr(product, "google_condition", ""),
                    "google_custom_product": getattr(
                        product, "google_custom_product", False
                    ),
                    "google_custom_label_0": getattr(
                        product, "google_custom_label_0", ""
                    ),
                    "google_custom_label_1": getattr(
                        product, "google_custom_label_1", ""
                    ),
                    "google_custom_label_2": getattr(
                        product, "google_custom_label_2", ""
                    ),
                    "google_custom_label_3": getattr(
                        product, "google_custom_label_3", ""
                    ),
                    "google_custom_label_4": getattr(
                        product, "google_custom_label_4", ""
                    ),
                    "variant_image": getattr(product, "variant_image", ""),
                    "variant_weight_unit": getattr(product, "variant_weight_unit", ""),
                    "variant_tax_code": getattr(product, "variant_tax_code", ""),
                    "cost_per_item": getattr(product, "cost_per_item", 0),
                    "included_japan": getattr(product, "included_japan", False),
                    "price_japan": getattr(product, "price_japan", 0),
                    "compare_at_price_japan": getattr(
                        product, "compare_at_price_japan", 0
                    ),
                    "included_international": getattr(
                        product, "included_international", False
                    ),
                    "price_international": getattr(product, "price_international", 0),
                    "compare_at_price_international": getattr(
                        product, "compare_at_price_international", 0
                    ),
                    "status": getattr(product, "status", ""),
                }
            )

        return formatted_products
