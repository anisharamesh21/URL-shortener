from flask import Flask, request, jsonify, redirect
import string
import random
from lrucache import LRUCache
from rate_limiter import RateLimiter
import sqlite3

app = Flask(__name__)

cache = LRUCache(capacity=6)
limiter = RateLimiter(capacity=3, refill_rate=1)

def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS urls(
                   short_code TEXT PRIMARY KEY,
                   long_url TEXT NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()

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
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)", (short_code, long_url))
    conn.commit()
    conn.close()
    cache.put(short_code, long_url)
    return jsonify({"short_code":short_code, "long_url":long_url})

@app.route("/<code>")
def redirect_to_url(code):
    cache_check = cache.get(code)
    if cache_check!=-1:
        print("cache hit")
        return redirect(cache_check)
    else:
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (code,))
        result = cursor.fetchone()
        conn.close()
        if result != None:
            print("cache miss")
            long_url = result[0]
            cache.put(code, long_url)
            return redirect(long_url)
    return "Not found", 404
    
init_db()
if __name__ == "__main__":
    app.run(debug=True)
