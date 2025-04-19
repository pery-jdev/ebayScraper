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
    *   **Translation:** Decide: Use official Google Cloud API or keep current libraries?
    *   **Price Fetching:** Decide: Implement APIs (eBay, Amazon, etc.) or expand scraping? Implement chosen methods for *all* required sources. Update eBay scraper to use dynamic queries.
    *   **Output:** Modify `save_to_csv` for the required format (translated names, individual prices).

## Workflow Diagram

```mermaid
flowchart TD
    A[Start] --> B{Read Input CSV};
    B --> C{Loop Through Products};
    C --> D[Translate Name (JP -> EN)];
    D --> E{Fetch Prices (USD/AUD)};
    subgraph E [Price Fetching]
        direction LR
        E1{Attempt APIs?}
        E1 -- Yes --> E2[Use eBay/Amazon/... API Clients]
        E1 -- No/Fallback --> E3[Use Scrapers (eBay/JapanTackle/...)]
        E2 --> E4[Store Prices]
        E3 --> E4
    end
    E --> F[Store Translated Name & Prices];
    F --> C;
    C -- End Loop --> G[Pass Products to Bundle Engine];
    G --> H{Generate Bundles & Leftovers};
    H --> I[Format Output Data];
    I --> J{Write Output CSV};
    J --> K[End];

    style E subgraph fill:#f9f,stroke:#333,stroke-width:2px
