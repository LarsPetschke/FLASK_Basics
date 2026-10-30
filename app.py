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


def fetch_post_by_id(post_id):
    """Return a single post by ID."""
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


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


@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        # Update fields
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")

        # Save updated list
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
