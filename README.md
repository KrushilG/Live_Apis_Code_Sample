# 🛍️ Flipkart Product Info Extraction API

A FastAPI-based microservice that extracts product details from Flipkart product URLs by parsing the `__INITIAL_STATE__` variable embedded in the HTML.

---

## 🚀 Features

* ✅ Validate Flipkart product URLs
* 🔍 Extract product metadata like title, price, image, rating, MRP, and discount
* 🧠 Parse embedded JavaScript object (`window.__INITIAL_STATE__`)
* 🔐 Simple API key-based usage limit (max 5 requests per API key)
* 📸 Dynamic image URL construction
* 🧭 Extract category breadcrumbs (l1 → l4)

---

## 📁 Project Structure

```plaintext
.
├── config.py            # Constants like headers, image size, defaults
├── extractor.py         # Main logic to fetch page and extract product info
├── utils.py             # Helpers: URL validation, image URL builder, API limit
├── main.py              # FastAPI app with `/get-product-info/` endpoint
└── README.md            # This file
```

---

## 🧑‍💻 Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/main-components-extractor-flipkart.git
cd main-components-extractor-flipkart
```

2. **Create a virtual environment and activate it**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🧪 API Usage

### 🔗 Endpoint

```http
POST /get-product-info/
```

### 🔖 Request Body

```json
{
  "url": "https://www.flipkart.com/product-name/p/itmXXXXX?pid=XYZ",
  "api": "123"
}
```

### ✅ Example Curl

```bash
curl -X POST http://127.0.0.1:8000/get-product-info/ \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.flipkart.com/some-product/p/itm123?pid=PID123", "api": "123"}'
```

---

## 🧾 Sample Response

```json
{
  "message": "Valid Flipkart product URL with PID.",
  "product_info": {
    "name": "Product Title",
    "price": "₹999",
    "image_url": "https://example.com/img.jpg",
    "discount": "25%",
    "mrp": "₹1299",
    "ratings_count": "120",
    "avg_rating": "4.3",
    "category_hierarchy": {
      "l1": "Electronics",
      "l2": "Mobiles",
      "l3": "Smartphones"
    }
  }
}
```

---

## 📌 Notes

* Maximum **5 requests per API key** (`api = "123"`).
* Ensure product URLs include a valid `pid` in the query string.
* Works only for **Flipkart product detail pages**.

---

## 🛠️ Developer Notes

* Product data is extracted from `window.__INITIAL_STATE__` using regex and `jmespath`.
* Custom user-agent and Chrome impersonation used for realistic requests (`curl_cffi`).
* Breadcrumb and image URL formatting handled dynamically.

---

## 📞 Contact

Maintained by **Darshit Rakhasiya**
Feel free to open an issue or submit a PR!
