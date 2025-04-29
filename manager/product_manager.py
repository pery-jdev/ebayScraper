from services.spider.ebay import EbaySpider
from services.bundles.bundle_engine import BundleEngine
import pandas as pd
import logging

class EbayProductManager:
    def __init__(self):
        self.ebay_spider = EbaySpider()
        self.logger = logging.getLogger(__name__)

    def get_products(self, query: str, category: str = None):
        try:
            products = self.ebay_spider.generate_products(query=query, category=category)
            
            # Format response sesuai kebutuhan API
            formatted_products = []
            for product in products:
                formatted_products.append({
                    'id': product.get('id'),
                    'name': product.get('name'),
                    'nameEn': product.get('name_en'),
                    'priceYen': product.get('price_yen'),
                    'priceUSD': product.get('price_usd'),
                    'priceAUD': product.get('price_aud'),
                    'url': product.get('url'),
                    'bundleGroup': product.get('bundle_group')
                })
            return formatted_products
            
        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            return []

    def generate_bundles(self, products_df, lures_per_bundle, min_usd_value, target_yen_per_lure):
        try:
            bundle_engine = BundleEngine(products_df.to_dict('records'))
            bundles, leftovers = bundle_engine.generate_bundles(
                lures_per_bundle=lures_per_bundle,
                min_usd_value=min_usd_value,
                target_yen_per_lure=target_yen_per_lure
            )
            
            # Gabungkan bundles dan leftovers
            all_items = bundles + leftovers
            return all_items
            
        except Exception as e:
            self.logger.error(f"Failed to generate bundles: {str(e)}")
            return []
