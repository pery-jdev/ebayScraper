from dataclasses import dataclass
from typing import List, Tuple

from dto.requests.product_request import ProductRequest

import csv


class BundleEngine:
    def __init__(self, products: List[ProductRequest]):
        self.products = products
        self.bundle_counter = 0

    def _validate_bundle(self, bundle: List[ProductRequest]) -> bool:
        """Validasi bundle dengan kriteria optimasi"""
        total_usd = sum(p.price_map["USD"] for p in bundle)
        total_aud = sum(p.price_map["AUD"] for p in bundle)
        avg_cost = sum(p.cost for p in bundle) / len(bundle)
        profit_margin = sum((p.price_map["USD"] * 0.85 - p.cost / 100) for p in bundle)

        return (
            len(bundle) == 6
            and total_usd >= 85  # Meningkatkan threshold USD
            and total_aud >= 120  # Meningkatkan threshold AUD
            and 800 <= avg_cost <= 880  # Memperketat range biaya
            and profit_margin >= 25  # Minimal $25 profit per bundle
        )

    def generate_bundles(
        self,
    ) -> Tuple[List[List[ProductRequest]], List[ProductRequest]]:
        """Generate bundle dengan optimasi profit margin"""
        if not self.products:
            self.products = self.generate_dummy_products()

        # Sort produk berdasarkan profit margin (USD tertinggi)
        sorted_products = sorted(
            self.products,
            key=lambda p: (p.price_map["USD"] / p.cost, p.price_map["USD"]),
            reverse=True,
        )

        # Alokasi greedy dengan priority queue
        bundles = []
        current_bundle = []

        for ProductRequest in sorted_products:
            temp_bundle = current_bundle + [ProductRequest]

            if len(temp_bundle) == 6:
                if self._validate_bundle(temp_bundle):
                    bundles.append(temp_bundle)
                    current_bundle = []
                else:
                    current_bundle = temp_bundle[:-1]  # Simpan sementara
            else:
                current_bundle.append(ProductRequest)

            # Cek jika current_bundle sudah bisa jadi valid bundle
            if len(current_bundle) >= 4 and self._validate_bundle(current_bundle):
                # Isi sisa slot dengan produk termurah
                while len(current_bundle) < 6:
                    cheapest = min(
                        (p for p in sorted_products if p not in current_bundle),
                        key=lambda p: p.cost,
                        default=None,
                    )
                    if cheapest:
                        current_bundle.append(cheapest)

                if self._validate_bundle(current_bundle):
                    bundles.append(current_bundle)
                    current_bundle = []

        # Final validation dan leftover handling
        valid_bundles = [b for b in bundles if self._validate_bundle(b)]
        used_ids = {p.id for bundle in valid_bundles for p in bundle}
        leftovers = [p for p in self.products if p.id not in used_ids]

        return valid_bundles, leftovers

    def save_to_csv(
        self, bundles: List[List[ProductRequest]], leftovers: List[ProductRequest]
    ):
        """Simpan hasil bundle ke CSV"""
        with open("data/bundles_report.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Bundle ID", "Product IDs", "Total USD", "Total AUD", "Average Yen"]
            )

            for i, bundle in enumerate(bundles, 1):
                writer.writerow(
                    [
                        f"BUNDLE-{i:03}",
                        ",".join(p.id for p in bundle),
                        sum(p.price_map["USD"] for p in bundle),
                        sum(p.price_map["AUD"] for p in bundle),
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
