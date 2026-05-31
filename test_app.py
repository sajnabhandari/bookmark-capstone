import pytest
from app import app as flask_app, parse_tags


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# --- parse_tags ---

def test_parse_tags_basic():
    assert parse_tags("python, web") == ["python", "web"]

def test_parse_tags_empty():
    assert parse_tags("") == []

def test_parse_tags_whitespace_only():
    assert parse_tags("   ") == []

def test_parse_tags_deduplication():
    assert parse_tags("python, Python, PYTHON") == ["python"]

def test_parse_tags_extra_commas():
    assert parse_tags(",python,,web,") == ["python", "web"]

def test_parse_tags_lowercases():
    result = parse_tags("Flask, FLASK")
    assert result == ["flask"]


# --- routes ---

def test_index_ok(client):
    r = client.get("/")
    assert r.status_code == 200

def test_add_get(client):
    r = client.get("/add")
    assert r.status_code == 200

def test_add_post_creates_bookmark(client):
    r = client.post("/add", data={"title": "Test", "url": "https://test.com", "tags": "t1"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Test" in r.data

def test_add_post_empty_ignored(client):
    from app import bookmarks
    before = len(bookmarks)
    client.post("/add", data={"title": "", "url": "", "tags": ""})
    assert len(bookmarks) == before

def test_tag_filter(client):
    client.post("/add", data={"title": "A", "url": "https://a.com", "tags": "alpha"})
    client.post("/add", data={"title": "B", "url": "https://b.com", "tags": "beta"})
    r = client.get("/?tag=alpha")
    html = r.data.decode()
    assert "https://a.com" in html
    assert "https://b.com" not in html

def test_search_title(client):
    client.post("/add", data={"title": "Unique Title XYZ", "url": "https://xyz.com", "tags": ""})
    r = client.get("/?q=unique+title+xyz")
    assert b"Unique Title XYZ" in r.data

def test_search_url(client):
    client.post("/add", data={"title": "URL Match", "url": "https://uniquedomain99.io", "tags": ""})
    r = client.get("/?q=uniquedomain99")
    assert b"URL Match" in r.data

def test_search_no_match(client):
    r = client.get("/?q=zzznomatch")
    assert b"No bookmarks match" in r.data


# --- student-written tests: key invariants ---

def test_bookmark_count_increases_by_one(client):
    # Invariant: every valid POST to /add adds exactly one bookmark, no more.
    from app import bookmarks
    before = len(bookmarks)
    client.post("/add", data={"title": "Count Test", "url": "https://count.io", "tags": "x"})
    assert len(bookmarks) == before + 1

def test_tag_and_search_compose(client):
    # Invariant: filtering by tag AND search query together narrows correctly.
    # Only the bookmark matching BOTH conditions should appear.
    client.post("/add", data={"title": "CSS Tricks", "url": "https://css-tricks.com", "tags": "css, web"})
    client.post("/add", data={"title": "CSS Zen Garden", "url": "https://csszengarden.com", "tags": "css, design"})
    r = client.get("/?tag=css&q=tricks")
    html = r.data.decode()
    assert "CSS Tricks" in html       # matches both tag and query
    assert "CSS Zen Garden" not in html  # has the tag but fails the query
