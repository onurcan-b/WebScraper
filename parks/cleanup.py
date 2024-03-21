import re
import json

# words to be ignored in indexing
INDEX_IGNORE = (
    "a",
    "an",
    "and",
    "&",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "chicago",
    "park",
    "parks",
)


def normalize_address(address):
    """
    This function takes an address and returns a normalized
    version of the address with extra whitespace removed.

    Parameters:
        * address:  a string representing an address

    Returns:
        A string representing the address with extra whitespace removed.
    """
    address_string = " ".join(address) if isinstance(address, list) else address
    return " ".join(address_string.split())


def clean_name(name):
    """
    This function takes a park name and removes any parenthesized portion.

    e.g. "Washington (George) Park" -> "Washington Park"

    Parameters:
        * name: a string representing a park name

    Returns:
        A string representing the park name with parenthesized portion removed.
    """
    # Learnt this method online on, Mr. Turk wanted me to include
    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    return re.sub(r"\s*\([^)]*\)", "", name).strip()


def tokenize(park):
    """
    This function takes a dictionary representing a park and returns a
    list of tokens that can be used to search for the park.

    The tokens should be a combination of the park's name, history, and
    description.

    All tokens should be normalized to lowercase, with punctuation removed as
    described in README.md.

    Tokens that match INDEX_IGNORE should be ignored.

    Parameters:
        * park:  a dictionary representing a park

    Returns:
        A list of tokens that can be used to search for the park.
    """
    items = ["name", "description", "history"]
    tokenized_set = set()  # Using a set to store all unique tokens

    for item in items:
        text = re.sub(r'[!.,\'"?:]', "", park[item])
        tokenized_set.update(
            {word.lower() for word in text.split() if word.lower() not in INDEX_IGNORE}
        )

    return list(tokenized_set)


def clean():
    """
    This function loads the parks.json file and writes a new file
    named normalized_parks.json that contains a normalized version
    of the parks data.
    """
    with open("parks.json", "r") as f:
        parks = json.load(f)

    for park in parks:
        park["address"] = normalize_address(park["address"])
        park["name"] = clean_name(park["name"])
        park["tokens"] = tokenize(park)

    with open("normalized_parks.json", "w") as f:
        json.dump(parks, f, indent=1)
