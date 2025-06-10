import json
import re
import logging
import asyncio
from typing import Any, List
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
        self.logger = logging.getLogger(__name__)

    def search_products(self, query: str):
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
            mode="httpx",
        )

        products = self.parser.parse_products(soup=response) # <- product list nya

        return products

    async def get_products(self, query: str):
        """Get products from eBay search results asynchronously"""
        try:
            # Get search results
            search_url = f"https://www.ebay.com.au/sch/i.html?_nkw={query}"
            response = await self.response.get_response_async(url=search_url, mode="httpx")
            products = self.parser.parse_products(soup=response)
            
            product_lists = []
            for product in products:
                # Get product details
                product_url = product.get("product_url")
                if not product_url:
                    continue
                    
                product_details = await self.get_product_details(product_url)
                if not product_details:
                    continue

                # Extract variant price
                variant_price = None
                if hasattr(product_details, "prices") and product_details.prices:
                    variant_price = product_details.prices.actual_price

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
                )
                product_lists.append(mapped_product)

            return product_lists
        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            return []

    async def get_product_details(self, url: str):
        """Get product details asynchronously"""
        try:
            response = await self.response.get_response_async(url=url, mode="httpx")
            product = self.parser.parse_product_details(soup=response)
            return product
        except Exception as e:
            self.logger.error(f"Failed to get product details: {str(e)}")
            return None

    def search_products_with_details(self, query: str):
        products = self.search_products(query=query)
        for product in products:
            product_details = self.get_product_details(product['product_url'])
            product['product_details'] = product_details
        return products

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
