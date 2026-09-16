from flask import Flask, request, jsonify, redirect
import string
import random

app = Flask(__name__)

url_map = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    short_code = "".join(random.choices(characters, k=length))
    return short_code
    pass

@app.route("/")
def home():
    return "The server is running"

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data["url"]
    short_code = generate_short_code(length=6)
    url_map[short_code]=long_url
    return jsonify({"short_code":short_code, "long_url":long_url})

@app.route("/<code>")
def redirect_to_url(code):
    if code in url_map:
        return redirect(url_map[code])
    else:
        return "404: Not found"
    


if __name__ == "__main__":
    app.run(debug=True)
