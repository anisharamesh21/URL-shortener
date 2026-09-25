## URL Shortener Project 
I built a URL shortener built with Flask, by utilizing a custom-built LRU cache and a token-bucket based rate limiter, along with SQLite for persistent storage.

## Features

- **Shorten URLs**: `POST /shorten` — takes in a long URL, returns a short code
- **Redirect**: `GET /<code>` — visiting a short code redirects to the original URL
- **LRU Cache**: recently accessed URLs are fetched from an in-memory cache (built from scratch using a hash map + doubly linked list) before checking the database, in order to make lookups faster
- **Rate Limiting**: a token-bucket based algorithm (built from scratch) that limits how many links a single IP address can create in a given time window, preventing misuse 
- **Persistent Storage**: URL mappings are stored in SQLite so that the links continue to work even when server restarts

## Tech Stack

- Python, Flask
- SQLite
- Custom built data structures: LRU Cache, Token Bucket Rate Limiter

## How It Works

1. A `POST` request to `/shorten` generates a random short code, stores the mapping in SQLite, and adds it to the LRU cache.
2. A `GET` request to `/<code>` checks the cache first. On a cache miss, it queries SQLite, then repopulates the cache for next time.
3. Every `/shorten` request is checked against a per-IP rate limiter before a new code is generated.

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then, in another terminal:

```bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

Visit the returned short code at `http://127.0.0.1:5000/<code>` to be redirected to the actual website.

## What I Learned

Building this from scratch (rather than using existing libraries for caching or rate limiting) solidified the core concepts through a series of interesting bugs — a type mismatch in the LRU-cache, a floating-point edge case in the rate limiter's token math, and a missing database commit that silently failed to persist data. Through this process, I was able to identify the motivation behind and potential of various data structures. Being able to use my custom-built parts to create this project exposed me to a real, complex working system. 