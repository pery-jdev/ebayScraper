import random
from services.bundles.bundle_engine import BundleEngine, Product
from services.pricing.currency_converter import CurrencyConverter
from services.spider.xe import XeSpider


def main():
    # alpha = AlphaVantageConverter()
    # xe_spider = XeSpider()
    # rates = alpha.get_rates()
    # # print(rates)

    # # rates = xe_spider.scrape_rate(10, "USD", "JPY", )
    # print(rates)
    converter = CurrencyConverter()
    convert = converter.convert_currency("USD", "JPY", 10)
    print(convert)

def test_bundle():
    sample_products = [
    Product(
        id="L001",
        name_jp="ジャクソン飛び過ぎダニエル 14g",
        name_en="Jackson Tobisugi Daniel 14g",
        cost=3200,
        cost_currency="JPY",
        price_map={
            "USD": 28.50,
            "AUD": 42.00,
            "EUR": 26.80  # Contoh currency tambahan
        },
        weight_g=14,
        category="Lure"
    ),
    Product(
        id="H205",
        name_jp="ガルプス フック 2Xストロング",
        name_en="Gamakatsu Hook 2X Strong",
        cost=4.20,
        cost_currency="EUR",  # Contoh cost currency berbeda
        price_map={
            "USD": 6.80,
            "AUD": 9.50,
            "EUR": 5.20
        },
        weight_g=2,
        category="Hook"
    ),
    Product(
        id="A012",
        name_jp="シーバス スーパーPEライン 150m",
        name_en="Seabass Super PE Line 150m",
        cost=5500,
        cost_currency="JPY",
        price_map={
            "USD": 52.00,
            "AUD": 75.00,
            "EUR": 48.00
        },
        weight_g=85,
        category="Accessory"
    )
]

    engine = BundleEngine(products=sample_products)
    bundles, leftovers = engine.generate_bundles()
    
    print("Generated Bundles:")
    for i, bundle in enumerate(bundles, 1):
        print(f"Bundle {i}:")
        for p in bundle:
            print(f"- {p.name_en} ({p.category})")
    
    print("\nLeftovers:", [p.name_en for p in leftovers])

if __name__ == "__main__":
    test_bundle()
