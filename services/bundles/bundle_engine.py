from typing import List, Tuple
from services.bundles.models import Product, Bundle
import uuid

import csv


class BundleEngine:
    def __init__(
        self,
        products: List[Product],
        lures_per_bundle: int = 6,
        min_usd_value: float = 75,
        target_yen_per_lure: float = 850,
    ):
        self.products = products
        self.lures_per_bundle = lures_per_bundle
        self.min_usd_value = min_usd_value
        self.target_yen_per_lure = target_yen_per_lure
        self.bundle_counter = 0

    def _validate_bundle(self, bundle: List[Product]) -> bool:
        """Validate bundle with configurable parameters"""
        if not bundle:
            return False

        total_usd = sum(p.price_usd for p in bundle)
        total_aud = sum(p.price_aud for p in bundle)

        return total_usd >= self.min_usd_value

    def generate_bundles(self) -> List[Bundle]:
        """Generate bundles with configurable parameters"""
        if not self.products:
            return []

        # Sort products by USD price (highest first)
        sorted_products = sorted(
            self.products,
            key=lambda p: p.price_usd,
            reverse=True,
        )

        # Greedy allocation
        bundles = []
        current_bundle = []

        for product in sorted_products:
            temp_bundle = current_bundle + [product]

            if len(temp_bundle) == self.lures_per_bundle:
                if self._validate_bundle(temp_bundle):
                    bundle_id = f"BUNDLE-{uuid.uuid4().hex[:8]}"
                    bundles.append(
                        Bundle(
                            id=bundle_id,
                            products=temp_bundle,
                            total_value_usd=sum(p.price_usd for p in temp_bundle),
                            total_value_aud=sum(p.price_aud for p in temp_bundle),
                        )
                    )
                    current_bundle = []
                else:
                    current_bundle = temp_bundle[:-1]  # Save temporarily
            else:
                current_bundle.append(product)

            # Check if current_bundle can be a valid bundle
            if len(current_bundle) >= (self.lures_per_bundle // 2) and self._validate_bundle(
                current_bundle
            ):
                # Fill remaining slots with cheapest products
                while len(current_bundle) < self.lures_per_bundle:
                    cheapest = min(
                        (p for p in sorted_products if p not in current_bundle),
                        key=lambda p: p.price_usd,
                        default=None,
                    )
                    if cheapest:
                        current_bundle.append(cheapest)

                if self._validate_bundle(current_bundle):
                    bundle_id = f"BUNDLE-{uuid.uuid4().hex[:8]}"
                    bundles.append(
                        Bundle(
                            id=bundle_id,
                            products=current_bundle,
                            total_value_usd=sum(p.price_usd for p in current_bundle),
                            total_value_aud=sum(p.price_aud for p in current_bundle),
                        )
                    )
                    current_bundle = []

        return bundles

    def save_to_csv(
        self, bundles: List[List[Product]], leftovers: List[Product]
    ):
        """Simpan hasil bundle ke CSV"""
        with open(
            "data/bundles_report.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Bundle ID",
                    "Product IDs",
                    "Total USD",
                    "Total AUD",
                    "Average Yen",
                ]
            )

            for i, bundle in enumerate(bundles, 1):
                writer.writerow(
                    [
                        f"BUNDLE-{i:03}",
                        ",".join(p.id for p in bundle),
                        sum(p.price_usd for p in bundle),
                        sum(p.price_aud for p in bundle),
                        sum(p.cost for p in bundle) / len(bundle),
                    ]
                )

            writer.writerow([])
            writer.writerow(["Leftover Products"])
            for p in leftovers:
                writer.writerow([p.id, p.name_en, p.cost])


# if __name__ == "__main__":
#     # Contoh penggunaan
#     engine = BundleEngine([])
#     bundles, leftovers = engine.generate_bundles()

#     print(f"Generated {len(bundles)} valid bundles:")
#     for i, bundle in enumerate(bundles, 1):
#         print(f"Bundle {i}: {[p.id for p in bundle]}")

#     print(f"\nLeftovers: {len(leftovers)} products")
#     engine.save_to_csv(bundles, leftovers)
#     print("\nReport saved to data/bundles_report.csv")
