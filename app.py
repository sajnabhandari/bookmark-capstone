from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory store — initialized once at startup
# Each bookmark: {id: int, title: str, url: str, tags: list[str]}
bookmarks: list[dict] = [
    {"id": 1, "title": "Flask Docs", "url": "https://flask.palletsprojects.com", "tags": ["python", "web"]},
]
_next_id: int = 2


def parse_tags(raw: str) -> list[str]:
    """Split comma-separated tag string into a cleaned, deduplicated list."""
    seen = set()
    result = []
    for tag in raw.split(","):
        t = tag.strip().lower()
        if t and t not in seen:
            seen.add(t)
            result.append(t)
    return result


def add_bookmark(title: str, url: str, tags: list[str]) -> dict:
    global _next_id
    bm = {"id": _next_id, "title": title, "url": url, "tags": tags}
    bookmarks.append(bm)
    _next_id += 1
    return bm


@app.route("/")
def index():
    tag_filter = request.args.get("tag", "").strip().lower()
    query = request.args.get("q", "").strip().lower()

    visible = bookmarks
    if tag_filter:
        visible = [b for b in visible if tag_filter in b["tags"]]
    if query:
        visible = [b for b in visible if query in b["title"].lower() or query in b["url"].lower()]

    all_tags = sorted({t for b in bookmarks for t in b["tags"]})
    return render_template("index.html", bookmarks=visible, all_tags=all_tags,
                           tag_filter=tag_filter, query=query)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        url = request.form.get("url", "").strip()
        raw_tags = request.form.get("tags", "")
        if title and url:
            tags = parse_tags(raw_tags)
            add_bookmark(title, url, tags)
        return redirect(url_for("index"))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
