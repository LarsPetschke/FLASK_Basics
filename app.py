import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "data.json"


def load_posts():
    """Load blog posts from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_posts(posts):
    """Save blog posts to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=4)


@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = load_posts()

        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        # Generate new ID
        new_id = max(post["id"] for post in posts) + 1 if posts else 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
