from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import is_valid_flipkart_url, validate_api, logger
from extractor import get_initial_state, extract_product_info
from datetime import datetime
from json import loads
from time import time
import uvicorn

app = FastAPI()

class URLRequest(BaseModel):
    url: str
    api: str

def main(user_input: str, api_key: str):
    if not (user_input.startswith("http://") or user_input.startswith("https://")):
        return False, 400, "Invalid input. Please enter a valid Flipkart product URL.", None

    if not is_valid_flipkart_url(user_input):
        return False, 400, "Invalid Flipkart URL or missing PID.", None

    is_valid, status_code, message = validate_api(api_key)
    if not is_valid:
        return False, status_code, message, None

    data = get_initial_state(user_input)
    if not data:
        return False, 500, "Failed to extract product JSON from page.", None

    product = extract_product_info(data)
    return True, 200, "Product info fetched successfully.", product
from fastapi.responses import JSONResponse

@app.post("/get-product-info/")
async def get_product_info(request: Request, url_request: URLRequest):
    client_ip = request.client.host
    req_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    body = await request.body()
    body_data = loads(body)

    s_time = time()
    success, status_code, message, product_data = main(url_request.url, url_request.api)
    e_time = time()
    execution_time = round(e_time - s_time, 2)

    if success:
        resp = {
            "query_params": body_data,
            "excution_time": execution_time,
            "success": True,
            "message": message,
            "data": product_data
        }
        logger(client_ip, body_data, req_time, status_code, url_request.api, resp)
        return JSONResponse(content=resp, status_code=200)
    else:
        resp = {
            "status_code": status_code,
            "message": message
        }
        logger(client_ip, body_data, req_time, status_code, url_request.api, resp)
        return JSONResponse(content=resp, status_code=status_code)



if __name__ == "__main__":
    uvicorn.run(app, host="51.222.244.92", port=1920)
