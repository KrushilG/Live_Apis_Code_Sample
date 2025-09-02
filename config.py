BASE_URL = "https://www.flipkart.com/%20/p/%20?pid="
DEFAULT_TEXT = "N/A"
HEIGHT_WIDTH = "900"
QUALITY = "100"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

from pymongo import MongoClient

CONN = MongoClient('mongodb://actowiz:tvvL4n%3D33%3D*_@51.222.244.92:27017/admin?authSource=admin')
DB = CONN.flipkart_api
KEY_COLLECTION = DB.key_tables
LOG_COLLECTION = DB.logs_table