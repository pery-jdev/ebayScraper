import pandas as pd
import logging

from services.spider.ebay import EbaySpider
from services.bundles.bundle_engine import BundleEngine
from services.pricing.currency_converter import CurrencyConverter


class EbayProductManager:
    def __init__(self):
        self.ebay_spider = EbaySpider()
        self.logger = logging.getLogger(__name__)
        self.currency_converter = CurrencyConverter()

    def get_products(self, query: str, category: str = None):
        try:
            products = self.ebay_spider.generate_products(
                query=query, category=category
            )
            products_list = products
            return products_list 


        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            return []
        
    def format_products(self, products):
        formatted_products = []
        for product in products:
            product_data = {
                
            }
        return formatted_products


    def test_product_detail(self):
        #! testing product detail
        detail = self.ebay_spider.get_product_details(
            url="https://www.ebay.com.au/itm/296469100027?_skw=lure+fishing&itmmeta=01JTDZ4ZM31RWX6G53D58EG4BH&hash=item4506ef75fb:g:srIAAOSwNcRmWSn3&itmprp=enc%3AAQAKAAAAwFkggFvd1GGDu0w3yXCmi1eZahIzPiFTwTzzospSpd0xQY%2B0nOl1%2BL%2FY2o9MXq9jSZdB3ZLJ1O5q4Ad9C74JFhRvc50gKpH%2FJBkGvyWLZ7uIEU9da0XOXQD9LVLjbACA1kRNkhowgyvVDfiBxyfSgbINx8rYDbUmPCmt2nYNSkr6ibAHwzDaVtPywQD7xUB9MKWUDFRiNBE8d6EkUGcVrSLvxbtebirXPMR--2H9DVVmO5I%2FdvyRzXLBjE7X9l1MTg%3D%3D%7Ctkp%3ABlBMUKr6k7_TZQ"
        )

        return detail

    def generate_bundles(
        self, products_df, lures_per_bundle, min_usd_value, target_yen_per_lure
    ):
        try:
            bundle_engine = BundleEngine(products_df.to_dict("records"))
            bundles, leftovers = bundle_engine.generate_bundles(
                lures_per_bundle=lures_per_bundle,
                min_usd_value=min_usd_value,
                target_yen_per_lure=target_yen_per_lure,
            )

            # Gabungkan bundles dan leftovers
            all_items = bundles + leftovers
            return all_items

        except Exception as e:
            self.logger.error(f"Failed to generate bundles: {str(e)}")
            return []
