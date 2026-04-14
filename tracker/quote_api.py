"""
tracker/quote_api.py

This file contains the quote API helper functions for the MySpend application.
"""

# jason used to convert API resonse to a Python dictionary
import json

# used to call external APIs, Requests is a popular library for making HTTP requests in Python. It simplifies the process of sending HTTP requests and handling responses.
from urllib.request import urlopen, Request

# used to handle URL errors when calling external APIs, such as network issues or invalid URLs. URLError is raised when there is a problem with the network connection or the URL is invalid, 
# while HTTPError is raised when the server returns an HTTP error status code (e.g., 404 Not Found, 500 Internal Server Error).
from urllib.error import URLError, HTTPError

#we use it for fallback qoutes if API is not working, it allows us to select a random quote from a predefined list of quotes.
import random


# This function calls an external API to get a random quote for the homepage. If the API call fails for any reason (network issues, API downtime, etc.), 
# it falls back to a predefined list of quotes to ensure that the homepage always has a quote to display. 
# The function returns a dictionary containing the quote text, author, and source (either "ZenQuotes" for API or "MySpend" for fallback).
#zenquotes.io is a free API that provides random inspirational quotes. But since it's a free service, it can sometimes be unreliable or slow. Also has no key and limited requests per hour. So we need a fallback mechanism to ensure that our app can still provide value to users even when the API is not working.

def get_home_quote():
    url = "https://zenquotes.io/api/random"

    fallback_quotes = [
        ("A budget is telling your money where to go instead of wondering where it went.", "Dave Ramsey"),
        ("Do not save what is left after spending, but spend what is left after saving.", "Warren Buffett"),
        ("Small daily money habits create long-term financial success.", "Arslan Hassan"),
        
    ]

    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urlopen(request, timeout=5)

        data = json.loads(response.read().decode("utf-8"))

        if isinstance(data, list) and len(data) > 0:
            quote = data[0]

            return {
                "text": quote.get("q", "Stay consistent with your money habits!"),
                "author": quote.get("a", "Arslan Hassan"),
                "source": "ZenQuotes"
            }

    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError):
        pass

    # fallback if API fails
    text, author = random.choice(fallback_quotes)

    return {
        "text": text,
        "author": author,
        "source": "MySpend"
    }