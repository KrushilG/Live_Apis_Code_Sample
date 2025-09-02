import re
import json
from curl_cffi import requests
import jmespath
from config import HEADERS, DEFAULT_TEXT
from utils import build_breadcrumbs, build_image_url

def get_initial_state(url):
    try:
        response = requests.get(url, headers=HEADERS, impersonate="chrome")
        if response.status_code != 200:
            print(f"Failed to retrieve page: {response.status_code}")
            return None

        if match := re.search(r'window\.__INITIAL_STATE__ = ({.*?});', response.text, re.DOTALL):
            initial_state = match[1]
            return json.loads(initial_state)
        else:
            print("window.__INITIAL_STATE__ not found in HTML.")
            return None
    except Exception as e:
        print(f"Error fetching/parsing URL: {e}")
        return None

def extract_product_info(data):
    product = {
        "name": jmespath.search(
            "pageDataV4.page.pageData.pageContext.titles.title", data
        )
        or DEFAULT_TEXT
    }

    product["price"] = jmespath.search("pageDataV4.page.pageData.pageContext.fdpEventTracking.events.psi.ppd.finalPrice", data) or DEFAULT_TEXT
    product["image_url"] = build_image_url(jmespath.search("pageDataV4.page.pageData.pageContext.imageUrl", data))

    product["discount"] = jmespath.search("pageDataV4.page.pageData.pageContext.pricing.totalDiscount", data) or DEFAULT_TEXT
    product["mrp"] = jmespath.search("pageDataV4.page.pageData.pageContext.pricing.mrp", data) or DEFAULT_TEXT

    product["ratings_count"] = jmespath.search("pageDataV4.page.pageData.pageContext.fdpEventTracking.commonContext.pr.ratingsCount", data) or DEFAULT_TEXT
    product["avg_rating"] = jmespath.search("pageDataV4.page.pageData.pageContext.fdpEventTracking.commonContext.pr.rating", data) or DEFAULT_TEXT

    product["category_hierarchy"] = build_breadcrumbs(data)
    return product
