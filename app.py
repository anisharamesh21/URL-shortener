from flask import Flask, request, jsonify
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
    


if __name__ == "__main__":
    app.run(debug=True)
