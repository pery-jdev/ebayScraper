import re

from typing import Any
from xml.etree.ElementTree import ParseError
from bs4 import BeautifulSoup
from decimal import Decimal, DecimalException

from dto.responses.currency_response import CurrencyResponse
from dto.requests.product_request_sdc import Prices, ProductRequestSDC as ProductRequest
from dto.requests.product_request_sdc import ProductDetailsRequestSDC as ProductDetailRequest
from services.spider.utils.xe_formatter import XeFormatter


class EbayParser:
    """Parser for eBay product listings and details
    """

    def __init__(self):
        self.product_lists: list[ProductRequest] = []

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

    # def parse_product_details(self, soup: BeautifulSoup):
    #     """Parse detailed product information from product page

    #     Args:
    #         soup: BeautifulSoup instance of eBay product detail page

    #     Returns:
    #         Complete ProductRequest object with:
    #         - variant_price: List of price options
    #         - image_src: List of all image URLs
    #         - vendor: Extracted brand information
    #         - type: Product category

    #     Raises:
    #         AttributeError: If required elements are missing
    #     """
    #     product_details: dict[str, str] = {}


    #     body = soup.find("div", attrs={"class": "tabs__content"})
    #     body_html = str(body) if body else None

    #     # prices
    #     prices_list = []
    #     prices = soup.find("div", attrs={"data-testid": "x-bin-price"})
    #     price_primary = None
    #     if prices:
    #         try:
    #             price_primary = prices.find("div", attrs={"class": "x-price-primary"}).text.strip()
    #             # price_primary = self.data_processor.extract_price(price_primary)
    #         except AttributeError:
    #             price_primary = ""

    #         try:
    #             actual_price = prices.find('div', attrs={'class':'x-additional-info__item--0'}).text.strip()
    #             # actual_price = self.data_processor.extract_price(actual_price)
    #         except AttributeError:
    #             actual_price = ""

    #     try:
    #         saving = prices.find('div', attrs={'class':'x-additional-info__item--1'}).text.strip()
    #         # saving = self.data_processor.extract_price(saving)
    #     except AttributeError:
    #         saving = ""

    #     product_details['prices'] = {
    #         'price_primary': price_primary,
    #         'actual_price': actual_price,
    #         'saving': saving
    #     }



    #     # images
    #     product_image_lists: list[str] = []
    #     try:
    #         images = soup.find("div", attrs={"data-testid": "x-photos"}).find_all(
    #             "button", attrs={"class": "ux-image-grid-item"}
    #         )
    #         for image in images:
    #             try:
    #                 image_url = image.find("img")["src"]
    #             except:
    #                 image_url = image.find("img")["data-src"]
    #             try:
    #                 image_alt = image.find("img")["alt"]
    #             except:
    #                 image_alt = ""

    #             image_data: dict[str, Any] = {
    #                "url": image_url,
    #                "alt": image_alt
    #            }
    #             product_image_lists.append(image_data)
    #     except:
    #         images = []

    #     # variant
    #     try:
    #         variant_sku = soup.find(
    #             "div",
    #             attrs=[
    #                 "class",
    #                 "ux-layout-section__textual-display ux-layout-section__textual-display--itemId",
    #             ],
    #         ).find("span", attrs={"class": "ux-textspans ux-textspans--BOLD"}).text.strip()
    #     except:
    #         pass

        
    #     try:
    #         items = soup.find(
    #             "div", attrs={"class": "ux-layout-section-evo ux-layout-section--features"}
    #         ).find_all("div", attrs={"class": "ux-layout-section-evo__row"})
    #         for item in items:
    #             item_cols = item.find_all(
    #                 "div", attrs={"class": "ux-layout-section-evo__col"}
    #             )
    #             for item_col in item_cols:
    #                 item_col_label = item_col.find(
    #                     "dt", attrs={"class": "ux-labels-values__labels"}
    #                 )
    #                 item_col_value = item_col.find(
    #                     "dd", attrs={"class": "ux-labels-values__values"}
    #                 )
    #                 if item_col_label and item_col_value:
    #                     product_details[item_col_label.text.strip()] = item_col_value.text.strip()
    #     except:
    #         items = []

    #     # product categories
    #     product_category = soup.find('nav', attrs={'class': 'breadcrumbs breadcrumb--overflow'}).find_all('li')
    #     categories = ", ".join([category.find('a').text.strip() for category in product_category])

    #     # posttage and shipping
    #     shipping = soup.find('div', attrs={'data-testid': 'ux-layout-section-module'}).find_all('div', attrs={'class': 'ux-labels-values'})
    #     for ship in shipping:
    #         shipping_label = ship.find('div', attrs={'class': 'ux-labels-values__labels-content'}).text.strip()
    #         shipping_value = ship.find('div', attrs={'class': 'ux-labels-values__values-content'}).text.strip()
    #         product_details[shipping_label] = shipping_value
        
    #     product_data: dict[str, Any] = {
    #         "body_html": body_html,
    #         "image_src": product_image_lists[0]['url'],
    #         "image_alt_text": product_image_lists[0]['alt'],
    #         "vendor": product_details.get("Brand", ""),
    #         "product_category": categories,
    #         "variant_sku": variant_sku,
    #         **product_details
    #     }
    #     return product_data

    def parse_product_details(self, soup: BeautifulSoup) -> ProductDetailRequest: # Mengubah tipe return
        """Parse detailed product information from product page

        Args:
            soup: BeautifulSoup instance of eBay product detail page

        Returns:
            ProductDetailsDTO object with parsed product information.
            (Docstring diperbarui untuk mencerminkan return DTO)

        Raises:
            AttributeError: If required elements are missing (bergantung pada implementasi error handling)
            IndexError: If product_image_lists kosong
        """
        product_details: dict[str, Any] = {} # Mengubah tipe value menjadi Any karena prices adalah dict


        body = soup.find("div", attrs={"class": "tabs__content"})
        body_html = str(body) if body else None

        # prices
        # Variabel price_primary, actual_price, saving tetap ada
        price_primary_val = None # Menggunakan _val untuk menghindari konflik jika ada field DTO dengan nama sama
        actual_price_val = ""
        saving_val = ""

        prices_element = soup.find("div", attrs={"data-testid": "x-bin-price"}) # Mengganti nama variabel prices
        if prices_element:
            try:
                price_primary_val = prices_element.find("div", attrs={"class": "x-price-primary"}).text.strip()
                # price_primary_val = self.data_processor.extract_price(price_primary_val)
            except AttributeError:
                price_primary_val = "" # Sesuai logika awal, default ke string kosong

            try:
                actual_price_val = prices_element.find('div', attrs={'class':'x-additional-info__item--0'}).text.strip()
                # actual_price_val = self.data_processor.extract_price(actual_price_val)
            except AttributeError:
                actual_price_val = ""
        
        # Bagian saving dipisah karena struktur try-except awal
        # Jika prices_element adalah None, prices_element.find akan error, jadi ini perlu penyesuaian
        if prices_element: # Hanya coba cari saving jika prices_element ada
            try:
                saving_val = prices_element.find('div', attrs={'class':'x-additional-info__item--1'}).text.strip()
                # saving_val = self.data_processor.extract_price(saving_val)
            except AttributeError:
                saving_val = ""
        else: # Jika prices_element tidak ada, saving juga tidak ada
            saving_val = ""


        # product_details['prices'] tidak lagi digunakan untuk menyimpan dict prices secara langsung
        # karena akan dimasukkan ke DTO Prices.
        # Namun, kita akan membuat instance DTO Prices di akhir.

        # images
        product_image_lists: list[dict[str, str]] = [] # Tipe diperjelas
        image_src_val = None
        image_alt_text_val = ""

        try:
            images_container = soup.find("div", attrs={"data-testid": "x-photos"})
            if images_container:
                images = images_container.find_all(
                    "button", attrs={"class": "ux-image-grid-item"}
                )
                for image in images:
                    image_url = ""
                    image_alt = ""
                    img_tag = image.find("img")
                    if img_tag:
                        image_url = img_tag.get("src") or img_tag.get("data-src", "")
                        image_alt = img_tag.get("alt", "")

                    image_data: dict[str, str] = {
                       "url": image_url,
                       "alt": image_alt
                    }
                    product_image_lists.append(image_data)
        except Exception: # Tangkap exception yang lebih umum jika ada masalah saat parsing gambar
            images = [] # Variabel images ini tidak digunakan di luar blok ini, jadi tidak apa-apa

        if product_image_lists:
            image_src_val = product_image_lists[0].get('url')
            image_alt_text_val = product_image_lists[0].get('alt', "")


        # variant
        variant_sku_val = None # Menggunakan _val
        try:
            sku_element = soup.find(
                "div",
                class_="ux-layout-section__textual-display ux-layout-section__textual-display--itemId",
            ) # Atribut class bisa disederhanakan
            if sku_element:
                bold_span = sku_element.find("span", class_="ux-textspans ux-textspans--BOLD")
                if bold_span:
                    variant_sku_val = bold_span.text.strip()
        except Exception:
            pass # Sesuai logika awal

        
        # Item specifics akan dimasukkan ke dalam dictionary product_details
        try:
            items_section = soup.find(
                "div", attrs={"class": "ux-layout-section-evo ux-layout-section--features"}
            )
            if items_section:
                items = items_section.find_all("div", attrs={"class": "ux-layout-section-evo__row"})
                for item in items:
                    item_cols = item.find_all(
                        "div", attrs={"class": "ux-layout-section-evo__col"}
                    )
                    for item_col in item_cols:
                        item_col_label_tag = item_col.find(
                            "dt", attrs={"class": "ux-labels-values__labels"}
                        )
                        item_col_value_tag = item_col.find(
                            "dd", attrs={"class": "ux-labels-values__values"}
                        )
                        if item_col_label_tag and item_col_value_tag:
                            label_text = item_col_label_tag.text.strip()
                            value_text = item_col_value_tag.text.strip()
                            # Membersihkan teks "... Read moreabout the condition" dari value Condition
                            if label_text == "Condition" and "Read more" in value_text:
                                value_text = value_text.split("Read more")[0].strip()
                            product_details[label_text] = value_text
        except Exception:
            items = [] # Variabel items ini tidak digunakan di luar blok ini

        # product categories
        categories_val = "" # Menggunakan _val
        try:
            product_category_nav = soup.find('nav', attrs={'class': 'breadcrumbs breadcrumb--overflow'})
            if product_category_nav:
                category_tags = product_category_nav.find_all('li')
                categories_list = [category.find('a').text.strip() for category in category_tags if category.find('a')]
                categories_val = ", ".join(categories_list)
        except Exception:
            pass # Menjaga agar tetap berjalan jika ada error

        # postage and shipping
        # Ini juga akan memasukkan data ke dalam dictionary product_details
        try:
            shipping_section = soup.find('div', attrs={'data-testid': 'ux-layout-section-module'}) # Mungkin perlu lebih spesifik
            if shipping_section: # Pastikan shipping_section ditemukan
                shipping_items = shipping_section.find_all('div', attrs={'class': 'ux-labels-values'})
                for ship_item in shipping_items: # Mengganti nama variabel ship
                    shipping_label_tag = ship_item.find('div', attrs={'class': 'ux-labels-values__labels-content'})
                    shipping_value_tag = ship_item.find('div', attrs={'class': 'ux-labels-values__values-content'})
                    if shipping_label_tag and shipping_value_tag:
                        label_text = shipping_label_tag.text.strip()
                        value_text = shipping_value_tag.text.strip()
                        product_details[label_text] = value_text
        except Exception:
            pass
        
        # --- Membuat instance DTO Prices ---
        prices_dto = Prices(
            price_primary=price_primary_val,
            actual_price=actual_price_val,
            saving=saving_val
        )

        # --- Membuat instance DTO ProductDetailsDTO ---
        # Menggunakan .get() untuk keamanan jika kunci tidak ada di product_details
        product_data_dto = ProductDetailRequest(
            body_html=body_html,
            image_src=image_src_val,
            image_alt_text=image_alt_text_val,
            vendor=product_details.get("Brand"), # vendor diambil dari Brand
            product_category=categories_val,
            variant_sku=variant_sku_val,
            prices=prices_dto,
            Condition=product_details.get("Condition"),
            Brand=product_details.get("Brand"),
            Bait_Type=product_details.get("Bait Type"), # Mapping dari nama dengan spasi
            Model=product_details.get("Model"),
            Item_Length=product_details.get("Item Length"), # Mapping dari nama dengan spasi
            Postage=product_details.get("Postage:"), # Mapping dari nama dengan :
            international_delivery_info=product_details.get(""), # Mapping dari kunci kosong
            Delivery=product_details.get("Delivery:") # Mapping dari nama dengan :
        )
        
        return product_data_dto

        

        



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
