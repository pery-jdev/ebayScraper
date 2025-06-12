import pandas as pd
import logging
import numpy as np
import asyncio
from typing import List, Dict, Any, Tuple
from services.spider.ebay import EbaySpider
from services.bundles.bundle_engine import BundleEngine
from services.bundles.models import Bundle, Product
from manager.currency_manager import CurrencyManager
from dto.requests.product_request import ProductRequest


class EbayProductManager:
    def __init__(self):
        self.ebay_spider = EbaySpider()
        self.logger = logging.getLogger(__name__)
        self.currency_manager = CurrencyManager()
        self._current_df = None

    async def get_products(self, query: str, category: str = None):
        try:
            products = await self.ebay_spider.generate_products(
                query=query, category=category
            )
            products_list = products
            return products_list

        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            return []

    async def search_products(self, query: str, category: str = None):
        try:
            products = await self.ebay_spider.search_products_with_details(query=query)
            products_list = products
            return products_list

        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            return []

    def format_products(self, products):
        return []  # Return empty list since we're not using the formatted products

    def test_product_detail(self):
        # Testing product detail
        base_url = "https://www.ebay.com.au/itm/296469100027"
        params = (
            "?_skw=lure+fishing"
            "&itmmeta=01JTDZ4ZM31RWX6G53D58EG4BH"
            "&hash=item4506ef75fb:g:srIAAOSwNcRmWSn3"
            "&itmprp=enc%3AAQAKAAAAwFkggFvd1GGDu0w3yXCmi1eZahIzPiFTwTzzospSpd0xQY"
            "%2B0nOl1%2BL%2FY2o9MXq9jSZdB3ZLJ1O5q4Ad9C74JFhRvc50gKpH%2FJBkGvyWLZ7uIEU9da0XOXQD"
            "9LVLjbACA1kRNkhowgyvVDfiBxyfSgbINx8rYDbUmPCmt2nYNSkr6ibAHwzDaVtPywQD7xUB9MKWUDFR"
            "iNBE8d6EkUGcVrSLvxbtebirXPMR--2H9DVVmO5I%2FdvyRzXLBjE7X9l1MTg%3D%3D%7Ctkp%3ABlBMUKr6k7_TZQ"
        )
        url = base_url + params
        detail = self.ebay_spider.get_product_details(url=url)

        return detail

    def generate_bundles(
        self,
        df: pd.DataFrame,
        lures_per_bundle: int,
        min_usd_value: float,
        target_yen_per_lure: float,
    ) -> Tuple[List[Bundle], List[Product]]:
        """
        Generate bundles from the DataFrame.
        Returns a tuple of (bundles, leftovers).
        """
        try:
            self.logger.info("Starting bundle generation...")

            df.to_json("df_before_bundling.json", orient="records", force_ascii=False)
            
            # Convert cost per item to float
            df['Cost per item'] = pd.to_numeric(df['Cost per item'], errors='coerce')
            
            # Calculate prices using approximate conversion rates
            df['price_aud'] = df['Cost per item']
            df['price_usd'] = df['Cost per item'] * 0.65  # Approximate AUD to USD
            df['price_jpy'] = df['Cost per item'] * 100  # Approximate AUD to JPY

            # Drop rows with NaN prices
            df = df.dropna(subset=["price_usd", "price_aud", "price_jpy"])
            
            if df.empty:
                self.logger.warning("No valid products with prices found for bundling")
                return [], []

            # Convert DataFrame to list of Product objects
            products = []
            for _, row in df.iterrows():
                product = Product(
                    title=row["Title"],
                    price_usd=float(row["price_usd"]),
                    price_aud=float(row["price_aud"]),
                )
                products.append(product)

            # Initialize bundle engine
            bundle_engine = BundleEngine(
                products=products,
                lures_per_bundle=lures_per_bundle,
                min_usd_value=min_usd_value,
                target_yen_per_lure=target_yen_per_lure,
            )

            # Generate bundles
            bundles = bundle_engine.generate_bundles()
            
            if not bundles:
                self.logger.warning("No bundles could be generated with the given parameters")
                return [], products

            # Get leftover products
            used_products = set()
            for bundle in bundles:
                used_products.update(bundle.products)
            leftovers = [p for p in products if p not in used_products]

            self.logger.info(
                f"Generated {len(bundles)} bundles with {len(leftovers)} leftover products"
            )
            return bundles, leftovers

        except Exception as e:
            self.logger.error(f"Failed to generate bundles: {str(e)}")
            return [], []

    async def add_pricing_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds USD and AUD pricing to the DataFrame by searching on eBay asynchronously.
        """
        self.logger.info("Adding pricing information to DataFrame...")
        # Create new columns for pricing if they don't exist
        if "price_usd" not in df.columns:
            df["price_usd"] = None
        if "price_aud" not in df.columns:
            df["price_aud"] = None

        # Store the DataFrame reference
        self._current_df = df

        # Process products in batches
        batch_size = 10
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i + batch_size]
            tasks = []
            
            # Create tasks for each product in the batch
            for index, row in batch_df.iterrows():
                translated_name = row.get("Handle", row.get("Title"))
                if translated_name:
                    tasks.append(self._process_product_pricing(index, translated_name))
            
            # Wait for all tasks in the batch to complete
            if tasks:
                await asyncio.gather(*tasks)

        self.logger.info("Finished adding pricing information.")
        return df

    async def _process_product_pricing(self, index: int, translated_name: str) -> None:
        """Process pricing for a single product asynchronously"""
        try:
            # Get products from eBay
            ebay_products = await self.ebay_spider.get_products(query=translated_name)

            if ebay_products:
                # Assuming the first result is the most relevant
                best_match = ebay_products[0]

                # Extract prices and clean them
                price_aud = best_match.variant_price
                if price_aud:
                    # Remove currency symbol and convert to float
                    price_aud = float(price_aud.replace("AU $", "").replace(",", "").strip())
                    
                    try:
                        # Use currency_manager to convert AUD to USD
                        price_usd = price_aud * 0.65  # Approximate AUD to USD conversion
                    except Exception as convert_e:
                        self.logger.error(
                            f"Currency conversion failed for {translated_name}: {convert_e}"
                        )
                        price_usd = None
                else:
                    price_aud = None
                    price_usd = None

                # Update DataFrame
                if self._current_df is not None:
                    self._current_df.loc[index, "price_aud"] = price_aud
                    self._current_df.loc[index, "price_usd"] = price_usd
                    self.logger.info(
                        f"Pricing added for {translated_name}: AUD={price_aud}, USD={price_usd}"
                    )
            else:
                self.logger.warning(
                    f"No products found on eBay for query: {translated_name}"
                )

        except Exception as e:
            self.logger.error(
                f"Error searching eBay for {translated_name}: {e}"
            )

    def preprocess_products_df(self, products_df: pd.DataFrame) -> pd.DataFrame:
        # Kolom string
        string_columns = [
            "Product Handle",
            "Product Title",
            "Body (HTML)",
            "Vendor or Brand Name",
            "Product Category",
            "Product Type",
            "Product Tags",
            "Option1 Name",
            "Option1 Value",
            "Option1 Linked To",
            "Option2 Name",
            "Option2 Value",
            "Option2 Linked To",
            "Option3 Name",
            "Option3 Value",
            "Option3 Linked To",
            "Variant SKU",
            "Variant Inventory Tracker",
            "Variant Inventory Policy",
            "Variant Fulfillment Service",
            "Variant Barcode",
            "Image Src",
            "Image Alt Text",
            "SEO Title",
            "SEO Description",
            "Google Shopping / Google Product Category",
            "Google Shopping / Gender",
            "Google Shopping / Age Group",
            "Google Shopping / MPN",
            "Google Shopping / Condition",
            "Google Shopping / Custom Label 0",
            "Google Shopping / Custom Label 1",
            "Google Shopping / Custom Label 2",
            "Google Shopping / Custom Label 3",
            "Google Shopping / Custom Label 4",
            "Variant Tax Code",
            "Variant Weight Unit",
            "status",
        ]
        for col in string_columns:
            if col in products_df.columns:
                products_df[col] = (
                    products_df[col].replace(np.nan, "", regex=True).astype(str)
                )

        # Kolom boolean
        bool_columns = [
            "Product Status Draft or Published",
            "Variant Requires Shipping",
            "Variant Taxable",
            "Gift Card",
            "Google Shopping / Custom Product",
            "Included / Japan",
            "Included / International",
        ]
        for col in bool_columns:
            if col in products_df.columns:
                products_df[col] = self.clean_bool_column(products_df[col])

        # Kolom list
        list_columns = ["Variant Price", "Variant Image"]
        for col in list_columns:
            if col in products_df.columns:

                def to_list(x):
                    if pd.isna(x):
                        return []
                    if isinstance(x, list):
                        return x
                    if hasattr(x, "result"):
                        return [str(x.result)]
                    return [str(x)]

                products_df[col] = products_df[col].apply(to_list)

        # Pastikan hasil translate berupa string di semua kolom string
        for col in string_columns:
            if col in products_df.columns:
                products_df[col] = products_df[col].apply(
                    lambda x: x.result if hasattr(x, "result") else x
                )
                products_df[col] = (
                    products_df[col].replace(np.nan, "", regex=True).astype(str)
                )

        # Field wajib: status
        if "status" not in products_df.columns:
            products_df["status"] = "active"

        # Kolom numerik (float)
        float_columns = ["Variant Grams", "Cost per item"]
        for col in float_columns:
            if col in products_df.columns:

                def to_float(x):
                    if hasattr(x, "result"):
                        try:
                            return float(x.result)
                        except Exception:
                            return None
                    try:
                        return float(x)
                    except Exception:
                        return None

                products_df[col] = products_df[col].apply(to_float)

        # Kolom numerik (int)
        int_columns = ["Image Position"]
        for col in int_columns:
            if col in products_df.columns:

                def to_int(x):
                    if pd.isna(x):
                        return 0  # Default number
                    if hasattr(x, "result"):
                        try:
                            return int(float(x.result))
                        except Exception:
                            return 0
                    try:
                        return int(float(x))
                    except Exception:
                        return 0

                products_df[col] = products_df[col].apply(to_int)

        return products_df

    @staticmethod
    def clean_bool_column(series):
        # Nilai yang dianggap True
        true_values = {True, "True", "true", 1, "1", "yes", "Yes", "y", "Y"}
        # Nilai yang dianggap False
        false_values = {
            False,
            "False",
            "false",
            0,
            "0",
            "no",
            "No",
            "n",
            "N",
            "",
            None,
            np.nan,
            float("nan"),
        }

        def to_bool(x):
            if x in true_values:
                return True
            return False

        return series.apply(to_bool)
