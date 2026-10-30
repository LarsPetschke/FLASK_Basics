import json
from flask import Flask, render_template

app = Flask(__name__)

def load_posts():
    """Load blog posts from JSON file."""
    with open("data.json", "r") as f:
        return json.load(f)

@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
rue)