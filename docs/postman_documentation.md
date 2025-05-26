# Postman Documentation for EbayScraper API

This document outlines the API endpoints for the EbayScraper project, which automates product translation, price searching (including eBay), and bundle creation for fishing lures.

**Base URL:** `http://localhost:8000` (Assuming the application runs on port 8000)

---

## 1. Root Endpoint

**GET `/api`**

A simple endpoint to check if the API is running.

### Request

`GET /api`

### Response (200 OK)

```json
{
  "message": "Hello World"
}
```

---

## 2. Search Products

**POST `/api/search`**

Searches for products based on a query and an optional category. This endpoint likely interacts with eBay to fetch product information.

### Request

`POST /api/search`
`Content-Type: application/x-www-form-urlencoded`

**Form Data:**

| Key      | Type   | Description                               | Required |
| -------- | ------ | ----------------------------------------- | -------- |
| `query`  | string | The search query for the product.         | Yes      |
| `category` | string | Optional category to narrow down the search. | No       |

### Example Request

```
POST /api/search
Content-Type: application/x-www-form-urlencoded

query=fishing%20lure&category=lures
```

### Response (200 OK)

```json
[
  {
    "product_name": "Example Fishing Lure",
    "price_usd": 15.99,
    "price_aud": 22.50,
    "source": "eBay"
  },
  {
    "product_name": "Another Lure",
    "price_usd": 10.00,
    "price_aud": 14.00,
    "source": "eBay"
  }
]
```

### Error Response (500 Internal Server Error)

```json
{
  "error": "Product search failed"
}
```

---

## 3. Translate Products

**POST `/api/translate`**

Translates product names from a provided CSV file (Japanese to English).

### Request

`POST /api/translate`
`Content-Type: multipart/form-data`

**Form Data:**

| Key    | Type | Description                               | Required |
| ------ | ---- | ----------------------------------------- | -------- |
| `file` | file | A CSV file containing product names to translate. | Yes      |

### Example CSV Input (`input.csv`)

```csv
Product Name,Cost in Yen,Other Attribute
ジャクソン飛び過ぎダニエル 14g,1500,Lure
シマノ バンタム,2000,Reel
```

### Example Request

```
POST /api/translate
Content-Type: multipart/form-data

--form 'file=@/path/to/your/input.csv;type=text/csv'
```

### Response (200 OK)

```json
[
  {
    "Product Name": "Jackson Tobisugi Daniel 14g",
    "Cost in Yen": 1500,
    "Other Attribute": "Lure"
  },
  {
    "Product Name": "Shimano Bantam",
    "Cost in Yen": 2000,
    "Other Attribute": "Reel"
  }
]
```

### Error Response (500 Internal Server Error)

```json
{
  "error": "Product translation failed"
}
```

---

## 4. Create Bundles

**POST `/api/bundle`**

Creates bundles of products based on specified rules from a provided CSV file.

### Request

`POST /api/bundle`
`Content-Type: multipart/form-data`

**Form Data:**

| Key                 | Type    | Description                               | Required |
| ------------------- | ------- | ----------------------------------------- | -------- |
| `file`              | file    | A CSV file containing product data.       | Yes      |
| `lures_per_bundle`  | integer | The exact number of lures per bundle (e.g., 6). | Yes      |
| `min_usd_value`     | float   | Minimum total overseas value in USD (e.g., 75.0). | Yes      |
| `target_yen_per_lure` | float   | Average cost per lure in Yen (e.g., 850.0). | Yes      |

### Example CSV Input (`product_data.csv`)

```csv
Product Name,Cost in Yen,Price USD,Price AUD
Jackson Tobisugi Daniel 14g,1500,12.50,18.00
Shimano Bantam,2000,16.00,23.00
...
```

### Example Request

```
POST /api/bundle
Content-Type: multipart/form-data

--form 'file=@/path/to/your/product_data.csv;type=text/csv'
--form 'lures_per_bundle=6'
--form 'min_usd_value=75.0'
--form 'target_yen_per_lure=850.0'
```

### Response (200 OK)

```json
{
  "bundles": [
    {
      "bundle_id": "bundle_1",
      "lures": [
        {"name": "Lure A", "price_usd": 15.0},
        {"name": "Lure B", "price_usd": 10.0},
        // ... 6 lures
      ],
      "total_usd_value": 80.0,
      "total_aud_value": 115.0,
      "average_yen_cost": 860.0
    }
  ],
  "leftovers": [
    {"name": "Leftover Lure X", "price_usd": 5.0}
  ]
}
```

### Error Response (500 Internal Server Error)

```json
{
  "error": "Bundle creation failed"
}
```

---

## 5. Convert Currency

**POST `/api/convert`**

Converts a given amount from one currency to another.

### Request

`POST /api/convert`
`Content-Type: application/x-www-form-urlencoded`

**Form Data:**

| Key           | Type    | Description                               | Required |
| ------------- | ------- | ----------------------------------------- | -------- |
| `amount`      | float   | The amount to convert.                    | Yes      |
| `from_currency` | string  | The currency to convert from (e.g., "USD"). | Yes      |
| `to_currency`   | string  | The currency to convert to (e.g., "AUD").   | Yes      |

### Example Request

```
POST /api/convert
Content-Type: application/x-www-form-urlencoded

amount=100.0&from_currency=USD&to_currency=AUD
```

### Response (200 OK)

```json
{
  "convertedAmount": 145.0
}
```

### Error Response (500 Internal Server Error)

```json
{
  "error": "Currency conversion failed"
}
```

---

## 6. Process File (Generic CSV Read)

**POST `/api/process`**

A generic endpoint to read and return the contents of a CSV file.

### Request

`POST /api/process`
`Content-Type: multipart/form-data`

**Form Data:**

| Key    | Type | Description                               | Required |
| ------ | ---- | ----------------------------------------- | -------- |
| `file` | file | The CSV file to process.                  | Yes      |

### Example Request

```
POST /api/process
Content-Type: multipart/form-data

--form 'file=@/path/to/your/any_file.csv;type=text/csv'
```

### Response (200 OK)

```json
[
  {
    "Column1": "Value1",
    "Column2": "Value2"
  },
  {
    "Column1": "Value3",
    "Column2": "Value4"
  }
]
```

### Error Response (500 Internal Server Error)

```json
{
  "error": "Internal Server Error"
}
```

---

## 7. Get Product Detail (Test Endpoint)

**GET `/api/detail`**

A test endpoint to retrieve product details.

### Request

`GET /api/detail`

### Response (200 OK)

```json
{
  "product_id": "test_id",
  "name": "Test Product",
  "price": 99.99
}
```

---

## 8. Run Full Pipeline

**POST `/api/pipeline`**

This endpoint executes the entire workflow:
1. Reads the input CSV file.
2. Translates product names (Japanese to English).
3. Searches for product prices (USD & AUD) from various sources, including eBay.
4. Creates bundles based on specified rules and identifies leftover lures.

### Request

`POST /api/pipeline`
`Content-Type: multipart/form-data`

**Form Data:**

| Key                 | Type    | Description                               | Required |
| ------------------- | ------- | ----------------------------------------- | -------- |
| `file`              | file    | A CSV file containing product data (e.g., "Product Name" in Japanese). | Yes      |
| `lures_per_bundle`  | integer | The exact number of lures per bundle (e.g., 6). | Yes      |
| `min_usd_value`     | float   | Minimum total overseas value in USD (e.g., 75.0). | Yes      |
| `target_yen_per_lure` | float   | Average cost per lure in Yen (e.g., 850.0). | Yes      |

### Example CSV Input (`input_products.csv`)

```csv
Title,Cost in Yen,Other Column
ジャクソン飛び過ぎダニエル 14g,1500,Lure
シマノ バンタム,2000,Reel
ダイワ ルアー,1200,Lure
...
```
**Note:** The `Title` column is expected for translation.

### Example Request

```
POST /api/pipeline
Content-Type: multipart/form-data

--form 'file=@/path/to/your/input_products.csv;type=text/csv'
--form 'lures_per_bundle=6'
--form 'min_usd_value=75.0'
--form 'target_yen_per_lure=850.0'
```

### Response (200 OK)

```json
{
  "bundles": [
    {
      "bundle_id": "bundle_1",
      "lures": [
        {"name": "Translated Lure A", "price_usd": 15.0, "price_aud": 21.0},
        // ... 6 lures
      ],
      "total_usd_value": 80.0,
      "total_aud_value": 115.0,
      "average_yen_cost": 860.0
    }
  ],
  "leftovers": [
    {"name": "Leftover Lure X", "price_usd": 5.0, "price_aud": 7.0}
  ],
  "translated_product_names": [
    {
      "Title": "Translated Lure A",
      "Cost in Yen": 1500,
      "Price USD": 15.0,
      "Price AUD": 21.0
    }
  ]
}
```

### Error Response (500 Internal Server Error)

```json
{
  "error": "Pipeline processing failed: [error message]"
}
