# Project Status Summary & Proposed Plan (As of 2025-04-20)

This document summarizes the current implementation status of the Python script for automating fishing lure bundling, based on code analysis.

## Requirements Overview

1.  **Translate Product Names (JP -> EN):** Use Google Cloud Translation API.
2.  **Search Product Prices (USD & AUD):** Use APIs (Amazon, eBay, Rakuten, Google Shopping) or scrape specific sites (JapanTackle, TackleWarehouse, Plat.co.jp).
3.  **Create Bundles:** 6 lures/bundle, >= $75 USD, >= $110 AUD, avg cost ~850 JPY.
4.  **Identify Leftovers:** List products not fitting into bundles.
5.  **Input:** Read product data from CSV.
6.  **Output:** Write new CSV with translated names, prices (USD/AUD), bundle group, total bundle price, and leftovers.

## Current Implementation Status

**Implemented / Partially Implemented:**

*   ✅ **Translation:** Uses third-party libraries (`translators`, `translatepy`) for JP -> EN translation. (`services/translations/translator.py`) (Requirement 1 - Partial)
*   ✅ **Price Fetching (eBay):** Scrapes eBay using Selenium/BeautifulSoup. (`services/spider/ebay.py`, `manager/product_manager.py`) (Requirement 2 - Partial)
*   ✅ **Currency Conversion:** Uses AlphaVantage API with XE.com scraping fallback. (`services/pricing/currency_converter.py`) (Part of Requirement 2)
*   ✅ **Bundling Logic:** Core logic exists, checks for 6 items and average Yen cost (800-880 range). (`services/bundles/bundle_engine.py`) (Requirement 3 - Mostly)
*   ✅ **Leftover Identification:** Correctly identifies products not fitting into bundles. (`services/bundles/bundle_engine.py`) (Requirement 4)
*   ✅ **Output Generation:** Basic CSV output (`data/bundles_report.csv`) for bundles (IDs, totals) and leftovers (ID, name, cost) exists via `save_to_csv`. (`services/bundles/bundle_engine.py`) (Requirement 6 - Partial)

**Missing / Gaps:**

*   ❌ **Official Google Cloud Translation API:** Not used as requested.
*   ❌ **Official eBay Browse API:** Not used; relies on scraping.
*   ❌ **Other Price Sources:** No implementation for Amazon API, Rakuten API, Google Shopping API, or scraping JapanTackle, TackleWarehouse, Plat.co.jp.
*   ❌ **Input CSV Reading:** No logic found to read the initial product data CSV. (Requirement 5)
*   ❌ **Workflow Integration:** No main script connecting all steps (Read -> Translate -> Price -> Bundle -> Write). `main.py` is for testing.
*   ⚠️ **Bundling Rule Discrepancy:** USD/AUD thresholds were $85/$120, **corrected to $75/$110** as per requirements. (Requirement 3)
*   ❌ **Output Format:** Needs adjustment to include translated names and individual product prices per bundle item in the output CSV. (Requirement 6)
*   ❌ **Dynamic Queries:** eBay scraping uses a static query ("Fishing Lures") instead of translated product names from the input. (Requirement 2)

## Proposed Plan / Next Steps

1.  **Input Processing:** Implement reading the input CSV (e.g., `data/product.csv`).
2.  **Workflow Orchestration:** Build the main script logic:
    *   Read CSV.
    *   Loop: Translate -> Fetch Prices (using translated names) -> Store Data.
    *   Bundle products.
    *   Write final CSV.
3.  **Refine Implementations:**
    *   **Translation:** Decide: Use official Google Cloud API or keep current libraries? (Assuming current libraries for now)
    *   **Price Fetching:** Decide: Implement APIs (eBay, Amazon, etc.) or expand scraping? (Assuming expanding scraping for now). Implement chosen methods for *all* required sources. Update eBay scraper to use dynamic queries.
    *   **Output:** Modify `save_to_csv` for the required format (translated names, individual prices).

## Detailed Workflow Diagram

```mermaid
flowchart TD
    A[Start main.py] --> B(Load Lures);
    subgraph B [Load Lures from CSV]
        direction LR
        B1[main.load_lures_from_csv] --> B2{"Read data/product.csv"};
        B2 --> B3["Create List[LureData]"];
    end

    B --> C{Process Each Lure};
    C -- For Each LureData --> D(Translate Name);
    subgraph D [Translate Name]
        direction LR
        D1[services.translations.MultiTranslator.translate_text] --> D2["Update LureData.name_en"];
    end

    D --> E(Fetch Prices);
    subgraph E [Fetch Prices (USD/AUD)]
        direction LR
        E1{Use APIs?}
        E1 -- Yes --> E2[API Clients (eBay, Amazon...)]
        E1 -- No/Fallback --> E3(Web Scrapers);
            subgraph E3 [Web Scrapers]
                direction TB
                E3a[services.spider.EbaySpider.get_products(query=LureData.name_en)]
                E3b[...]
                E3c[Other Scrapers (JapanTackle...)]
            end
        E2 --> E4{Parse Prices}
        E3 --> E4
        E4 --> E5[services.pricing.CurrencyConverter (if needed)]
        E5 --> E6["Update LureData.price_map{'USD': ..., 'AUD': ...}"]
    end

    E --> C;
    C -- End Loop --> F(Pass Processed Lures);
    F -- List[LureData] --> G(Generate Bundles);
    subgraph G [Generate Bundles]
        direction LR
        G1[services.bundles.BundleEngine.__init__(products=List[LureData])] --> G2[BundleEngine.generate_bundles];
        G2 --> G3["Validate Bundles (check rules)"];
        G3 --> G4["Return (valid_bundles, leftovers)"];
    end

    G --> H(Save Report);
    subgraph H [Save Report]
        direction LR
        H1[services.bundles.BundleEngine.save_to_csv] --> H2{"Format Data (Names, Prices, etc.)"};
        H2 --> H3["Write data/bundles_report.csv"];
    end

    H --> I[End];

    style B subgraph fill:#lightblue,stroke:#333,stroke-width:2px
    style D subgraph fill:#lightgreen,stroke:#333,stroke-width:2px
    style E subgraph fill:#lightcoral,stroke:#333,stroke-width:2px
    style G subgraph fill:#lightyellow,stroke:#333,stroke-width:2px
    style H subgraph fill:#lightgrey,stroke:#333,stroke-width:2px
