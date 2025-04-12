import random
from services.bundles.bundle_engine import BundleEngine
from services.pricing.currency_converter import CurrencyConverter
from services.spider.xe import XeSpider
from dto.requests.product_request import ProductRequest

from manager.product_manager import EbayProductManager

def test_converter():
    # alpha = AlphaVantageConverter()
    # xe_spider = XeSpider()
    # rates = alpha.get_rates()
    # # print(rates)

    # # rates = xe_spider.scrape_rate(10, "USD", "JPY", )
    # print(rates)
    converter = CurrencyConverter()
    convert = converter.convert_currency("USD", "JPY", 10)
    print(convert)


# def test_bundle():
#     sample_products = [
#         Product(
#             id="L001",
#             name_jp="ジャクソン飛び過ぎダニエル 14g",
#             name_en="Jackson Tobisugi Daniel 14g",
#             cost=3200,
#             cost_currency="JPY",
#             price_map={
#                 "USD": 28.50,
#                 "AUD": 42.00,
#                 "EUR": 26.80,  # Contoh currency tambahan
#             },
#             weight_g=14,
#             category="Lure",
#         ),
#         Product(
#             id="H205",
#             name_jp="ガルプス フック 2Xストロング",
#             name_en="Gamakatsu Hook 2X Strong",
#             cost=4.20,
#             cost_currency="EUR",  # Contoh cost currency berbeda
#             price_map={"USD": 6.80, "AUD": 9.50, "EUR": 5.20},
#             weight_g=2,
#             category="Hook",
#         ),
#         Product(
#             id="A012",
#             name_jp="シーバス スーパーPEライン 150m",
#             name_en="Seabass Super PE Line 150m",
#             cost=5500,
#             cost_currency="JPY",
#             price_map={"USD": 52.00, "AUD": 75.00, "EUR": 48.00},
#             weight_g=85,
#             category="Accessory",
#         ),
#     ]

#     engine = BundleEngine(products=sample_products)
#     bundles, leftovers = engine.generate_bundles()

#     print("Generated Bundles:")
#     for i, bundle in enumerate(bundles, 1):
#         print(f"Bundle {i}:")
#         for p in bundle:
#             print(f"- {p.name_en} ({p.category})")

#     print("\nLeftovers:", [p.name_en for p in leftovers])


def test_product():
    products = [
        ProductRequest(
            handle="nike-airmax-2023",
            title="Nike Air Max 2023",
            vendor="Nike",
            type="Shoes",
            tags="sports, running, sneakers",
            published=True,
            option1_name="Size",
            option1_value="42",
            variant_price=[149.99, 159.99],
            variant_inventory_tracker="shopify",
            variant_grams=500.0,
            variant_requires_shipping=True,
            variant_taxable=True,
            image_src=[
                "https://example.com/images/nike-airmax-2023-front.jpg",
                "https://example.com/images/nike-airmax-2023-side.jpg",
            ],
            variant_image=[
                "https://example.com/images/nike-airmax-2023-variant1.jpg",
                "https://example.com/images/nike-airmax-2023-variant2.jpg",
            ],
            status="active",
        ),
        ProductRequest(
            handle="adidas-ultraboost-2023",
            title="Adidas Ultraboost 2023",
            vendor="Adidas",
            type="Shoes",
            tags="sports, running, comfort",
            published=True,
            option1_name="Size",
            option1_value="41",
            variant_price=[180.00, 190.00],
            variant_inventory_tracker="shopify",
            variant_grams=480.0,
            variant_requires_shipping=True,
            variant_taxable=True,
            image_src=[
                "https://example.com/images/adidas-ultraboost-2023-front.jpg",
                "https://example.com/images/adidas-ultraboost-2023-side.jpg",
            ],
            variant_image=[
                "https://example.com/images/adidas-ultraboost-2023-variant1.jpg"
            ],
            status="active",
        ),
        ProductRequest(
            handle="puma-running-x",
            title="Puma Running X",
            vendor="Puma",
            type="Shoes",
            tags="running, lightweight, breathable",
            published=False,
            option1_name="Size",
            option1_value="40",
            variant_price=[120.50, 130.75],
            variant_inventory_tracker="shopify",
            variant_grams=450.0,
            variant_requires_shipping=True,
            variant_taxable=True,
            image_src=["https://example.com/images/puma-running-x-front.jpg"],
            variant_image=[
                "https://example.com/images/puma-running-x-variant1.jpg",
                "https://example.com/images/puma-running-x-variant2.jpg",
            ],
            status="draft",
        ),
        ProductRequest(
            handle="reebok-zig-kinetica",
            title="Reebok Zig Kinetica",
            vendor="Reebok",
            type="Shoes",
            tags="training, energy return, futuristic",
            published=True,
            option1_name="Size",
            option1_value="43",
            variant_price=[135.00, 145.00],
            variant_inventory_tracker="shopify",
            variant_grams=520.0,
            variant_requires_shipping=True,
            variant_taxable=True,
            image_src=[
                "https://example.com/images/reebok-zig-kinetica-front.jpg",
                "https://example.com/images/reebok-zig-kinetica-side.jpg",
            ],
            variant_image=[],
            status="active",
        ),
        ProductRequest(
            handle="newbalance-fresh-foam",
            title="New Balance Fresh Foam",
            vendor="New Balance",
            type="Shoes",
            tags="cushioning, stability, running",
            published=True,
            option1_name="Size",
            option1_value="39",
            variant_price=[160.00],
            variant_inventory_tracker="shopify",
            variant_grams=490.0,
            variant_requires_shipping=True,
            variant_taxable=True,
            image_src=[],
            variant_image=[
                "https://example.com/images/newbalance-fresh-foam-variant1.jpg"
            ],
            status="active",
        ),
    ]

    print(products)

def test_scraper():
    product_manager = EbayProductManager()
    products = product_manager.get_products()
    print(products)


if __name__ == "__main__":
    test_scraper()
