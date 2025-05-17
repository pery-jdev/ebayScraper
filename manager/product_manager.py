import pandas as pd
import logging

from services.spider.ebay import EbaySpider
from services.bundles.bundle_engine import BundleEngine
from services.pricing.currency_converter import CurrencyConverter
from dto.requests.product_request import ProductRequest


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
            # Konversi DataFrame ke list of ProductRequest agar BundleEngine tidak error
            products = [ProductRequest(**row) for row in products_df.to_dict("records")]
            bundle_engine = BundleEngine(products)
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

    def add_pricing_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds USD and AUD pricing to the DataFrame by searching on eBay.
        """
        self.logger.info("Adding pricing information to DataFrame...")
        # Create new columns for pricing if they don't exist
        if 'price_usd' not in df.columns:
            df['price_usd'] = None
        if 'price_aud' not in df.columns:
            df['price_aud'] = None

        # Iterate through the DataFrame and search for each product
        for index, row in df.iterrows():
            translated_name = row.get('Translated Name', row.get('Product Name')) # Assuming translated name is in 'Translated Name' column or fallback to 'Product Name'
            if translated_name:
                try:
                    # Call the spider's get_products method
                    # Note: This method returns a list, we might need logic to select the best match
                    ebay_products = self.ebay_spider.get_products(query=translated_name)

                    if ebay_products:
                        # Assuming the first result is the most relevant or you need logic to select
                        best_match = ebay_products[0]

                        # Extract prices
                        # The price is stored in variant_price after get_products processes it
                        price_usd = None # Placeholder, need to check how get_products handles USD vs AUD
                        price_aud = best_match.variant_price # Assuming variant_price is AUD based on ebay.com.au base_url

                        # Convert AUD to USD if necessary
                        if price_aud is not None:
                            try:
                                # Need to use currency_converter to convert AUD to USD
                                # Assuming currency_converter.calculate_price_map returns a dict like {'USD': amount_in_usd}
                                converted_prices = self.currency_converter.calculate_price_map(amount=price_aud, from_currency='AUD')
                                price_usd = converted_prices.get('USD')
                            except Exception as convert_e:
                                self.logger.error(f"Currency conversion failed for {translated_name}: {convert_e}")
                                price_usd = None # Set to None if conversion fails

                        # Update DataFrame
                        df.loc[index, 'price_aud'] = price_aud
                        df.loc[index, 'price_usd'] = price_usd
                        self.logger.info(f"Pricing added for {translated_name}: AUD={price_aud}, USD={price_usd}")

                    else:
                        self.logger.warning(f"No products found on eBay for query: {translated_name}")

                except Exception as e:
                    self.logger.error(f"Error searching eBay for {translated_name}: {e}")

            else:
                 self.logger.warning(f"No translated name available for row {index}, skipping pricing search.")

        self.logger.info("Finished adding pricing information.")
        return df
