import re

from typing import Any
from xml.etree.ElementTree import ParseError
from bs4 import BeautifulSoup
from decimal import Decimal, DecimalException

from dto.responses.currency_response import CurrencyResponse
from dto.requests.product_request_sdc import ProductRequestSDC as ProductRequest
from services.spider.utils.xe_formatter import XeFormatter
from services.processors.data_processor import DataProcessor


class EbayParser:
    """Parser for eBay product listings and details

    Maps eBay product data to ProductRequest DTO with the following key conversions:

    | eBay Field            | DTO Field            | Transformation Needed          |
    |-----------------------|----------------------|---------------------------------|
    | product_sku           | handle               | Direct mapping                 |
    | title                 | title                | Direct mapping                 |
    | price_primary         | variant_price        | Convert currency string to float list |
    | product_images[*].url | image_src            | Extract URLs from image dicts  |
    | Brand (from details)  | vendor               | Extract from product attributes |
    | Category (from details)| type                | Extract from product attributes |
    """

    def __init__(self):
        self.product_lists: list[ProductRequest] = []
        self.data_processor = DataProcessor()

    def parse_products(self, soup: BeautifulSoup) -> list[dict[str, Any]]:
        products: list[dict[str, Any]] = []
        """Parse product listings from search results page

        Args:
            soup: BeautifulSoup instance of eBay search results page

        Returns:
            List of ProductRequest objects with basic product info

        Notes:
            - Extracts title, price, and primary image
            - Uses listing ID as handle
            - Sets default vendor as 'eBay'
        """

        products_container = soup.find("ul", attrs={"class": "srp-results srp-list clearfix"})
        if not products_container:
            return []

        for product in products_container.find_all("li", class_="s-item"):
            title = product.find("div", class_="s-item__title")
            title = title.find("span", role="heading").text.strip() if title else ""

            price = product.find("span", class_="s-item__price")
            price = price.text.strip() if price else ""

            image = product.find("img", class_="s-item__image-img")
            image_url = image["src"] if image else ""

            product_url = product.find("a", class_="s-item__link")
            product_url = product_url["href"] if product_url else ""


            vendor = "eBay"  # Default vendor
            data_dict: dict[str, Any] = {
                "handle": product_url,
                "title": title,
                "vendor": vendor,
                "variant_price": price,
                "image_src": image_url,
                "product_url": product_url
            }

            products.append(data_dict)

        return products

    def parse_product_details(self, soup: BeautifulSoup) -> ProductRequest:
        """Parse detailed product information from product page

        Args:
            soup: BeautifulSoup instance of eBay product detail page

        Returns:
            Complete ProductRequest object with:
            - variant_price: List of price options
            - image_src: List of all image URLs
            - vendor: Extracted brand information
            - type: Product category

        Raises:
            AttributeError: If required elements are missing
        """
        product_details: dict[str, str] = {}


        body = soup.find("div", attrs={"class": "tabs__content"})
        body_html = str(body) if body else None

        # prices
        prices_list = []
        prices = soup.find("div", attrs={"data-testid": "x-bin-price"})
        price_primary = None
        if prices:
            try:
                price_primary = prices.find("div", attrs={"class": "x-price-primary"}).text.strip()
                price_primary = self.data_processor.extract_price(price_primary)
            except AttributeError:
                price_primary = ""

            try:
                actual_price = prices.find('div', attrs={'class':'x-additional-info__item--0'}).text.strip()
                actual_price = self.data_processor.extract_price(actual_price)
            except AttributeError:
                actual_price = ""

        try:
            saving = prices.find('div', attrs={'class':'x-additional-info__item--1'}).text.strip()
            saving = self.data_processor.extract_price(saving)
        except AttributeError:
            saving = ""

        product_details['prices'] = {
            'price_primary': price_primary,
            'actual_price': actual_price,
            'saving': saving
        }



        # images
        product_image_lists: list[str] = []
        try:
            images = soup.find("div", attrs={"data-testid": "x-photos"}).find_all(
                "button", attrs={"class": "ux-image-grid-item"}
            )
            for image in images:
                try:
                    image_url = image.find("img")["src"]
                except:
                    image_url = image.find("img")["data-src"]
                try:
                    image_alt = image.find("img")["alt"]
                except:
                    image_alt = ""

                image_data: dict[str, Any] = {
                   "url": image_url,
                   "alt": image_alt
               }
                product_image_lists.append(image_data)
        except:
            images = []

        # variant
        try:
            variant_sku = soup.find(
                "div",
                attrs=[
                    "class",
                    "ux-layout-section__textual-display ux-layout-section__textual-display--itemId",
                ],
            ).find("span", attrs={"class": "ux-textspans ux-textspans--BOLD"}).text.strip()
        except:
            pass

        
        try:
            items = soup.find(
                "div", attrs={"class": "ux-layout-section-evo ux-layout-section--features"}
            ).find_all("div", attrs={"class": "ux-layout-section-evo__row"})
            for item in items:
                item_cols = item.find_all(
                    "div", attrs={"class": "ux-layout-section-evo__col"}
                )
                for item_col in item_cols:
                    item_col_label = item_col.find(
                        "dt", attrs={"class": "ux-labels-values__labels"}
                    )
                    item_col_value = item_col.find(
                        "dd", attrs={"class": "ux-labels-values__values"}
                    )
                    if item_col_label and item_col_value:
                        product_details[item_col_label.text.strip()] = item_col_value.text.strip()
        except:
            items = []

        # product categories
        product_category = soup.find('nav', attrs={'class': 'breadcrumbs breadcrumb--overflow'}).find_all('li')
        categories = ", ".join([category.find('a').text.strip() for category in product_category])
        
        product_data: dict[str, Any] = {
            "body_html": body_html,
            "image_src": product_image_lists[0]['url'],
            "image_alt_text": product_image_lists[0]['alt'],
            "vendor": product_details.get("Brand", ""),
            "product_category": categories,
            "variant_sku": variant_sku,
            **product_details
        }
        return product_data

        

        



class XeParser:
    def __init__(self):
        self.formatter: XeFormatter = XeFormatter()

    def parse_rates(self, soup: BeautifulSoup):
        """Parse currency conversion data from raw text"""
        # Regex pattern untuk menangkap format: X [CUR1] = Y [CUR2]
        rate_pattern = r"""
            (\d+[\d,.]*)       # Jumlah mata uang asal (group 1)
            \s*([A-Z]{3})      # Kode mata uang asal (group 2)
            \s*=\s*
            ([\d,]+\.\d+)      # Jumlah mata uang tujuan (group 3)
            \s*([A-Z]{3})      # Kode mata uang tujuan (group 4)
        """

        # Regex pattern untuk total konversi: = Z [Currency Name]
        amount_pattern = r"""
            =\s*
            ([\d,]+\.\d+)      # Jumlah total (group 1)
            \s*([A-Za-z\s]+)   # Nama mata uang (group 2)
        """

        conversion = soup.find(
            "div", attrs={"class": "[grid-area:conversion]"}
        ).find_all("p")
        amount = conversion[0].text.strip()
        converted_amount = conversion[1].text.strip()
        base_rate = conversion[2].text.strip()
        dst_rate = conversion[3].text.strip()

        # process

        print(
            f"ammount: {amount}|| converted_amount: {converted_amount}|| base_rate: {base_rate}|| dst_rate: {dst_rate}"
        )  # print(converted_amount, '||', amount, '||', base_rate, '||', dst_rate)
        # print(conversion)

    def parse_rate(self, soup: BeautifulSoup) -> CurrencyResponse:
        """Parse currency conversion data from XE.com HTML content

        Args:
            soup: BeautifulSoup instance of XE.com conversion page

        Returns:
            CurrencyResponse with parsed conversion data

        Raises:
            ParseError: If any required data elements are missing
            ValueError: If numeric parsing fails
        """
        conversion = soup.find("div", attrs={"class": "[grid-area:conversion]"})
        if not conversion:
            raise ParseError("Conversion container not found")

        paragraphs = conversion.find_all("p")
        if len(paragraphs) < 4:
            raise ParseError("Insufficient conversion data paragraphs")

        try:
            # Parse numeric values
            amount_str = paragraphs[0].text.strip()  # Format: "100.00 USD"
            result_str = paragraphs[1].text.strip()  # Format: "14,800.00 JPY"
            rate_str = paragraphs[2].text.strip()  # Format: "1 USD = 148.00 JPY"

            # Extract currency codes using improved regex
            currency_match = re.search(r"(\b[A-Z]{3}\b).*?(\b[A-Z]{3}\b)", rate_str)
            if not currency_match:
                raise ParseError("Currency pair pattern not found")

            currency_pair = f"{currency_match.group(1)}_{currency_match.group(2)}"

            # Clean and convert numeric values
            amount = Decimal(re.sub(r"[^\d.]", "", amount_str))
            result = Decimal(re.sub(r"[^\d.]", "", result_str))
            rate = Decimal(re.sub(r"[^\d.]", "", rate_str.split("=")[1]))

            return CurrencyResponse.from_conversion(
                amount=amount,
                rate=rate,
                currency_pair=currency_pair,
                method="web_scraping",
            )

        except (IndexError, DecimalException, AttributeError) as e:
            raise ParseError(f"Error parsing conversion data: {str(e)}") from e
