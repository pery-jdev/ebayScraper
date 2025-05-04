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

            # Format response sesuai kebutuhan API
            formatted_products = []
            for product in products:

                formatted_products.append(
                    {
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
                )
            return formatted_products

        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            return []
        

    def test_product_detail(self):
        #! testing product detail
        detail = self.ebay_spider.get_product_details(
            url="https://www.ebay.com/itm/163300123513?hash=item2b6f8e2e55:g:K7sAAOSwZ~xV9DZ1"
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
