from flask import Flask, request, jsonify, redirect
import string
import random
from lrucache import LRUCache
from rate_limiter import RateLimiter

app = Flask(__name__)

url_map = {}
cache = LRUCache(capacity=6)
limiter = RateLimiter(capacity=3, refill_rate=1)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    short_code = "".join(random.choices(characters, k=length))
    return short_code
    

@app.route("/")
def home():
    return "The server is running"

@app.route("/shorten", methods=["POST"])
def shorten():
    address = request.remote_addr
    print("request from", address)
    if not limiter.check_request(address):
        return "Too many requests", 429
    data = request.get_json()
    long_url = data["url"]
    short_code = generate_short_code(length=6)
    url_map[short_code]=long_url
    cache.put(short_code, long_url)
    return jsonify({"short_code":short_code, "long_url":long_url})

@app.route("/<code>")
def redirect_to_url(code):
    cache_check = cache.get(code)
    if cache_check!=-1:
        print("cache hit")
        return redirect(cache_check)
    else:
        if code in url_map:
            print("cache miss")
            cache.put(code, url_map[code])
            return redirect(url_map[code])
    return "Not found", 404
    

if __name__ == "__main__":
    app.run(debug=True)
