I need a Python script that will automate the following tasks for my fishing lure business:

1. Translate Product Names (Japanese to English)

Use Google Cloud Translation API to translate product names in a CSV file.
Example Input: "ジャクソン飛び過ぎダニエル 14g"
Expected Output: "Jackson Tobisugi Daniel 14g"
2. Search for Product Prices Online (USD & AUD)

Fetch live pricing for each translated product from international fishing gear retailers.
Preferred methods:
Amazon API (Amazon Product Advertising API)
eBay API (eBay Browse API)
Rakuten API (Japanese tackle shops)
Google Shopping API (if needed)
If APIs are not available, use web scraping to extract prices from sites like:
JapanTackle.com
TackleWarehouse.com
Plat.co.jp
3. Create Bundles Based on Specific Rules

Each bundle must:
✅ Contain exactly 6 lures
✅ Have a total overseas value of at least $75 USD and $110 AUD
✅ Have an average cost per lure of around 850 yen

4. Identify Leftover Lures

If some lures do not fit into bundles, list them separately.
📝 Input File:
The script should read a CSV file that contains product data, including:
Product Name (in Japanese)
Cost in Yen
Other attributes (if needed)
📤 Output Requirements:
The script should output a new CSV file with:
Translated product names
Overseas pricing (USD & AUD)
Assigned bundle group
Total bundle price
Leftover products (if any)

langkah langkah apa yang harus saya lakukan dalam project saya ketika project briefnya seperti diatas bisa jelaskan?