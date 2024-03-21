import sys
import json
import lxml.html
from .utils import make_request, make_link_absolute
from .cleanup import normalize_address


def scrape_park_page(url="https://scrapple.fly.dev/parks/1"):
    """
    This function takes a URL to a park page and returns a
    dictionary with the title, address, description,
    and history of the park.

    Parameters:
        * url:  a URL to a park page

    Returns:
        A dictionary with the following keys:
            * url:          the URL of the park page
            * name:         the name of the park
            * address:      the address of the park
            * description:  the description of the park
            * history:      the history of the park
    """
    park_page = make_request(url)
    root = lxml.html.fromstring(park_page.text)

    name = root.xpath('//div[@class="page-title"]/h2[@class="section"]/text()')[0]

    address = root.xpath('//p[@class="address"]//text()')
    print(address)

    description = ""
    history = ""

    # Next sibling of the h3 that contains desc
    description_div = root.xpath(
        '//h3[contains(.,"Description")]/following-sibling::div[@class="block-text"]'
    )
    print(description_div)
    if description_div:
        description = " ".join(
            [d.strip() for d in description_div[0].xpath(".//text()")]
        )

    # Next sibling of the h3 that contains hist
    history_div = root.xpath(
        '//h3[contains(.,"History")]/following-sibling::div[@class="block-text"]'
    )
    print(history_div)
    if history_div:
        history = " ".join([h.strip() for h in history_div[0].xpath(".//text()")])

    return {
        "url": url,
        "name": name,
        "address": normalize_address(address),
        "description": description,
        "history": history,
    }


def get_park_urls(url):
    """
    This function takes a URL to a page of parks and returns a
    list of URLs to each park on that page.

    Parameters:
        * url:  a URL to a page of parks

    Returns:
        A list of URLs to each park on the page.
    """
    parks_list = make_request(url)
    root = lxml.html.fromstring(parks_list.text)

    links = root.xpath('//td/a[@href and contains(text(), "Details")]/@href')
    urls = [make_link_absolute(link, url) for link in links]

    return urls


def get_next_page_url(url):
    """
    This function takes a URL to a page of parks and returns a
    URL to the next page of parks if one exists.

    If no next page exists, this function returns None.
    """
    parks_list = make_request(url)
    root = lxml.html.fromstring(parks_list.text)
    next_url = root.xpath(
        '//a[contains(@class, "button") and contains(text(), "Next")]/@href'
    )

    if next_url:
        next_url = make_link_absolute(next_url[0], url)
        return next_url
    else:
        return None


def crawl(max_parks_to_crawl):
    """
    This function starts at the base URL for the parks site and
    crawls through each page of parks, scraping each park page
    and saving output to a file named "parks.json".

    Parameters:
        * max_parks_to_crawl:  the maximum number of pages to crawl
    """
    list_page_url = "https://scrapple.fly.dev/parks"
    parks = []
    urls_visited = 0

    while list_page_url and urls_visited < max_parks_to_crawl:
        park_urls = get_park_urls(list_page_url)

        for park_url in park_urls:
            if urls_visited >= max_parks_to_crawl:
                break
            park_data = scrape_park_page(park_url)
            parks.append(park_data)
            urls_visited += 1
        # Get the URL of the next page
        list_page_url = get_next_page_url(list_page_url)

    print("Writing parks.json")
    with open("parks.json", "w") as f:
        json.dump(parks, f, indent=1)


if __name__ == "__main__":
    """
    Tip: It can be convenient to add small entrypoints to submodules
         for ease of testing.

    In this file, we call scrape_park_page with a given URL and pretty-print
    the output.

    This allows testing that function from the command line with:

    $ python -m parks.crawler https://scrapple.fly.dev/parks/4

    Feel free to modify/change this if you wish, you won't be graded on this code.
    """
    from pprint import pprint

    if len(sys.argv) != 2:
        print("Usage: python -m parks.crawler <url>")
        sys.exit(1)
    result = scrape_park_page(sys.argv[1])
    pprint(result)
