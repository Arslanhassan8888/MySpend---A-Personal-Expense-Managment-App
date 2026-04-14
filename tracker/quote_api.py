"""
tracker/quote_api.py
--------------------
This file contains helper code for retrieving a quote
for the MySpend homepage.

It first tries to get a quote from an external API.
If that fails, it uses a fallback quote stored in the application.
"""

# json is used to convert the API response into a Python dictionary or list.
import json

# Request and urlopen are used to send a request to the external quote API
# and read the response returned by the server.
from urllib.request import urlopen, Request

# URLError and HTTPError are used to handle problems when calling the API,
# such as connection issues, invalid URLs, or server-side errors.
from urllib.error import URLError, HTTPError

# random is used to choose a fallback quote if the API is unavailable.
import random


# STEP 1: Get a homepage quote
def get_home_quote() -> dict:
    """
    Retrieve a quote for the homepage.

    This function:
    - sends a request to the ZenQuotes API
    - reads and converts the response into Python data
    - returns the quote text, author, and source
    - uses a fallback quote if the API request fails

    Returns:
        dict: A dictionary containing:
            - text: the quote content
            - author: the name of the author
            - source: where the quote came from
    """

    # API endpoint used to request one random quote
    url = "https://zenquotes.io/api/random"

    # Fallback quotes used if the API is unavailable
    fallback_quotes = [
        ("A budget is telling your money where to go instead of wondering where it went.", "Dave Ramsey"),
        ("Do not save what is left after spending, but spend what is left after saving.", "Warren Buffett"),
        ("Small daily money habits create long-term financial success.", "Arslan Hassan"),
    ]

    try:
        # Create the request with a browser-style header
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        # Send the request and wait up to 5 seconds for a response
        response = urlopen(request, timeout=5)

        # Convert the JSON response into Python data
        data = json.loads(response.read().decode("utf-8"))

        # The API returns a list, so check that it contains at least one quote
        if isinstance(data, list) and len(data) > 0:
            quote = data[0]

            # Return the quote details using fallback values if any field is missing
            return {
                "text": quote.get("q", "Stay consistent with your money habits!"),
                "author": quote.get("a", "Arslan Hassan"),
                "source": "ZenQuotes"
            }

    # If the API fails, ignore the error and use a fallback quote instead
    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError):
        pass

    # Choose one fallback quote at random
    text, author = random.choice(fallback_quotes)

    return {
        "text": text,
        "author": author,
        "source": "MySpend"
    }