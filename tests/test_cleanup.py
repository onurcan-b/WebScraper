import pytest
from parks.cleanup import normalize_address, tokenize, clean_name


def test_normalize_address_trimmed():
    assert (
        normalize_address(" \n 123 Main St Chicago, IL 60637 \n")
        == "123 Main St Chicago, IL 60637"
    )


def test_normalize_address_whitespace():
    assert (
        normalize_address("123 Main St       \n  Chicago, IL 60637")
        == "123 Main St Chicago, IL 60637"
    )


@pytest.fixture
def test_park():
    return {
        "name": "Washington (George) Park",
        "history": "Designed by Frederick Law Olmsted & Calvert Vaux",
        "description": "Located in the Washington Park/Woodlawn neighborhood, Washington Park totals 345.67 acres and features two gymnasiums, a photography lab, dance studio, racquetball court, fitness center,game room, and multi-purpose rooms",
        "address": "      5531 S. King Dr. \n    Chicago, IL 60615",
        "url": "https://scrapple.fly.dev/parks/581",
    }


def test_tokenize(test_park):
    tokens = set(tokenize(test_park))
    expected = {
        "washington",
        "(george)",
        "designed",
        "frederick",
        "law",
        "olmsted",
        "calvert",
        "vaux",
        "located",
        "park/woodlawn",
        "neighborhood",
        "totals",
        "34567",
        "acres",
        "features",
        "two",
        "gymnasiums",
        "photography",
        "lab",
        "dance",
        "studio",
        "racquetball",
        "court",
        "fitness",
        "centergame",
        "room",
        "multi-purpose",
        "rooms",
    }
    extra_tokens = tokens - expected
    missing_tokens = expected - tokens

    if extra_tokens:
        pytest.fail(f"Extra tokens: {extra_tokens}")
    if missing_tokens:
        pytest.fail(f"Missing tokens: {missing_tokens}")


def test_clean_name():
    assert clean_name("Washington (George) Park") == "Washington Park"
    assert clean_name("Admin Building") == "Admin Building"
    assert clean_name("Archer (William Beatty) Park") == "Archer Park"