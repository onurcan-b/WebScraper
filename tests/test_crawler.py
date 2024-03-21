from parks.crawler import scrape_park_page, get_park_urls, get_next_page_url


def test_scrape_park_page():
    url = "https://scrapple.fly.dev/parks/581"
    data = scrape_park_page(url)
    assert data["name"] == "Washington (George) Park"
    assert "5531 S. King Dr" in data["address"]
    assert "60615" in data["address"]
    assert "Located in the Washington Park/Woodlawn" in data["description"]
    assert "Frederick Law Olmsted" in data["history"]
    assert data["url"] == url

def test_scrape_park_page_2():
    url = "https://scrapple.fly.dev/parks/7"
    data = scrape_park_page(url)
    assert data["name"] == "Admin Building"
    assert "541 N. Fairbanks" in data["address"]
    assert "60611" in data["address"]
    assert "" in data["description"]
    assert data["history"] == ""
    assert data["url"] == url


def test_scrape_park_page_3():
    url = "https://scrapple.fly.dev/parks/17"
    data = scrape_park_page(url)
    assert data["name"] == "Archer (William Beatty) Park"
    assert "Kilbourn" in data["address"]
    assert "gymnasium, kitchen, and fitness center" in data["description"]
    assert "Abraham Lincoln" in data["history"]
    assert data["url"] == url

def test_get_park_urls():
    url = "https://scrapple.fly.dev/parks"
    urls = get_park_urls(url)
    assert len(urls) == 10
    assert urls[0] == "https://scrapple.fly.dev/parks/1"


def test_get_next_page_url():
    url = "https://scrapple.fly.dev/parks"
    next_url = get_next_page_url(url)
    assert next_url == "https://scrapple.fly.dev/parks?page=2"


def test_get_next_page_url_end():
    url = "https://scrapple.fly.dev/parks?page=62"
    next_url = get_next_page_url(url)
    assert next_url is None
