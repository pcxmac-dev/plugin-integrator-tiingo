"""What Tiingo's plugin attaches to (plugin API 2.2, liminal_libs.sources.apis): Tiingo's REST API, as Tiingo's pages
said on 2026-11-11 (the documentation at tiingo.com/documentation, each section's page read that day; the pricing
page's two tables, an individual's and a business's). One card for the whole plugin, its stocks (`tiingo`) and its
forex (`tiingofx`) alike: the app draws a plugin's APIs and its parts' once each, by name.

The user, 2026-11-11: "each plugin should reflect the the API its attached to, and present links that provide
documentation, the plugin interface should more or less contain what it already has, BUT, it should also expose more of
what the API is about". So every part of the API is named (`areas`: the documentation's sections), each said used here
or not, and the calls the plugin makes (`used`) beside the notable ones it does not.

Tiingo's site answers any address under /documentation/ with a page, a wrong one too: each page here was read, not
only asked for."""
from __future__ import annotations

from liminal_libs.sources.apis import Api, Area, Call, Link

from .client import SUPPORTED_TICKERS

API = "https://api.tiingo.com"
DOCS = "https://www.tiingo.com/documentation"
TOKEN = "https://www.tiingo.com/account/api/token"  # where the token is (the plugin's `signup`)
EOD, IEX, BOATS, FX = "End-of-Day", "IEX", "BOATS Overnight", "Forex"


def _docs(path: str) -> str:
    return f"{DOCS}/{path}"


TIINGO_REST = Api(
    name="Tiingo REST API",
    maker="Tiingo",
    about=("Tiingo's REST API serves end-of-day prices of US and Chinese stocks, ETFs and mutual funds from 1962, "
           "intraday bars from IEX, Blue Ocean's overnight session and its own 24x5 consolidated feed, forex and crypto, "
           "news, fundamentals and corporate actions. One token reaches all of it; the plan sets the requests an hour "
           "and a day, the different symbols a month and the bandwidth."),
    kind="rest",
    base=API,
    auth=("an API token (the account's API token page), sent as an Authorization: Token header (the plugin's way; a "
          "token query parameter works too); the supported-tickers file on apimedia.tiingo.com is asked without it"),
    limits=("Starter (free): 50 requests an hour, 1,000 a day, 500 different symbols and 1 GB a month; Power: 10,000 an "
            "hour, 100,000 a day, 40 GB a month; Commercial: 20,000 an hour, 150,000 a day, 100 GB a month. No "
            "rate-limit headers in its answers (none seen, 2026-10-27)"),
    costs=("Starter is free; Power $30 a month or $300 a year (an individual's), Commercial $50 a month or $499 a year (a "
           "business's internal use, up to two developers); the fundamentals are an add-on, redistribution and "
           "Enterprise priced by Tiingo's sales; Blue Ocean's real-time data needs its entitlement on the account"),
    links=(
        Link("Documentation", _docs("general/overview"), "docs"),
        Link("Connecting", _docs("general/connecting"), "auth"),
        Link("Symbology", _docs("appendix/symbology"), "guide"),
        Link("Pricing and limits", "https://www.tiingo.com/about/pricing", "pricing"),
        Link("Status page", "https://status.tiingo.com", "status"),
        Link("Uptime", "https://uptime.tiingo.com", "status"),
        Link("Changelog", _docs("general/changelog"), "changelog"),
        Link("API token", TOKEN, "console"),
        Link("Terms of service", "https://www.tiingo.com/tos", "terms"),
    ),
    areas=(
        Area(EOD, "daily prices of US and Chinese stocks, ETFs and mutual funds from 1962, raw and adjusted, each "
             "ticker's record; the supported-tickers file", _docs("end-of-day"),
             covered="the stocks' whole daily history (the US from 1962, the A-shares from 2007), split-adjusted here "
                     "from its split factors; an A-share's record; the supported-tickers file (TIINGO_LISTINGS on)"),
        Area(IEX, "IEX's top of book and last sale, and its intraday bars", _docs("iex"),
             covered="the scan: a day of AAPL's IEX minutes"),
        Area(BOATS, "Blue Ocean's overnight session (20:00-03:59 ET): top of book, last sale and minute bars (beta)",
             _docs("boats"),
             covered="Blue Ocean's nights live on a paid plan (tiingo (blue ocean)): the last sale and quote of the stocks "
                     "open on a chart, and their minutes of the night; the scan's probe"),
        Area("24x5 Consolidated", "Tiingo's real-time US equity feed from exchanges, ATS and OTC venues, Sunday 20:00 to "
             "Friday 20:00 ET, on every plan", _docs("equity-realtime-stock-data")),
        Area(FX, "currency pairs' top of book and intraday bars (beta)", _docs("forex"),
             covered="currency pairs' 1-minute bars from 2020 (its forex feed, tiingofx); the scan's probe"),
        Area("Crypto", "crypto pairs' bars across exchanges, and their records", _docs("crypto"),
             covered="the scan: a day of BTCUSD's minutes"),
        Area("News", "news articles by ticker, tag and source; bulk downloads for institutions", _docs("news"),
             covered="the scan: one article tells a paid plan from Starter"),
        Area("Fundamentals", "statements, daily metrics (market cap, P/E, P/B), definitions and company records: an "
             "add-on, the Dow 30 free to evaluate", _docs("fundamentals"),
             covered="the scan: ROKU's market cap for a day tells whether the add-on is on"),
        Area("Fund fees", "mutual funds' and ETFs' fee data (enterprise and institutional clients)",
             _docs("mutual-fund-and-etf-fees")),
        Area("Dividends", "distributions and distribution yields (an early release)", _docs("corporate-actions/dividends")),
        Area("Splits", "splits by day or by ticker (an early release)", _docs("corporate-actions/splits")),
        Area("Search", "tickers across asset classes by name or symbol (beta)", _docs("utilities/search")),
        Area("WebSockets", "firehoses of IEX, forex, crypto, 24x5 and BOATS updates (a separate API, "
             "wss://api.tiingo.com)", _docs("websockets")),
    ),
    calls=(
        Call("GET /tiingo/daily/{ticker}/prices", "a ticker's daily prices over a range, raw and adjusted, with its "
             "dividends and split factors", EOD,
             used="a stock's whole daily history in one request (from 1950-01-01: all it has), split-adjusted here; the "
                  "scan's first probe", docs=_docs("end-of-day")),
        Call("GET /tiingo/daily/{ticker}", "a ticker's record: name, exchange, description, first and last day", EOD,
             used="an A-share's record: its name, exchange and first day", docs=_docs("end-of-day")),
        Call(f"GET {SUPPORTED_TICKERS}", "every ticker Tiingo serves, with its exchange, asset type and dates (a zip, "
             "updated daily)", EOD,
             used="the A-shares' listings, with TIINGO_LISTINGS on: about 10 MB, no key sent", docs=_docs("end-of-day")),
        Call("GET /tiingo/fx/prices", "currency pairs' intraday bars (its pages show the one-pair form, "
             "/tiingo/fx/<ticker>/prices)", FX,
             used="a pair's minutes, three whole UTC days a request, asked with tickers= (the forex feed, tiingofx); the "
                  "scan's probe", docs=_docs("forex")),
        Call("GET /iex/{ticker}/prices", "a ticker's intraday bars from IEX", IEX,
             used="the scan: a day of AAPL's IEX minutes", docs=_docs("iex")),
        Call("GET /boats/{ticker}/prices", "a ticker's overnight bars on Blue Ocean", BOATS,
             used="a stock's minutes of the night under way (tiingo (blue ocean), a paid plan); the scan's probe",
             docs=_docs("boats")),
        Call("GET /boats/", "the overnight top of book and last sale of every ticker, or of those asked", BOATS,
             used="the last sale and quote of the stocks open on a chart, one request for them all (tickers=), every few "
                  "seconds of a night", docs=_docs("boats")),
        Call("GET /tiingo/crypto/prices", "crypto pairs' bars, real time and historical", "Crypto",
             used="the scan: a day of BTCUSD's minutes", docs=_docs("crypto")),
        Call("GET /tiingo/news", "the newest articles, by ticker, tag or source", "News",
             used="the scan: one article (only a paid plan's token is served)", docs=_docs("news")),
        Call("GET /tiingo/fundamentals/{ticker}/daily", "a company's daily metrics: market cap, enterprise value, P/E, "
             "P/B", "Fundamentals", used="the scan: ROKU's market cap for a day (the add-on)", docs=_docs("fundamentals")),
        Call("GET /iex", "every ticker's IEX top of book and last sale", IEX, docs=_docs("iex")),
        Call("GET /iex/{ticker}", "one ticker's IEX top of book and last sale", IEX, docs=_docs("iex")),
        Call("GET /boats/{ticker}", "one ticker's overnight top of book and last sale", BOATS, docs=_docs("boats")),
        Call("GET /tiingo/equity/intraday", "every ticker's 24x5 reference price and liquidity", "24x5 Consolidated",
             docs=_docs("equity-realtime-stock-data")),
        Call("GET /tiingo/equity/intraday/{ticker}/prices", "a ticker's 24x5 intraday bars", "24x5 Consolidated",
             docs=_docs("equity-realtime-stock-data")),
        Call("GET /tiingo/fx/top", "currency pairs' top of book", FX, docs=_docs("forex")),
        Call("GET /tiingo/crypto", "crypto pairs' records", "Crypto", docs=_docs("crypto")),
        Call("GET /tiingo/news/bulk_download", "the news archive's bulk files (institutional clients)", "News",
             docs=_docs("news")),
        Call("GET /tiingo/fundamentals/{ticker}/statements", "a company's quarterly and annual statements",
             "Fundamentals", docs=_docs("fundamentals")),
        Call("GET /tiingo/fundamentals/definitions", "the fundamental fields and what each is", "Fundamentals",
             docs=_docs("fundamentals")),
        Call("GET /tiingo/fundamentals/meta", "companies' records: sector, industry, reporting currency, filings",
             "Fundamentals", docs=_docs("fundamentals")),
        Call("GET /tiingo/funds/{ticker}", "a fund's record and share classes (enterprise clients)", "Fund fees",
             docs=_docs("mutual-fund-and-etf-fees")),
        Call("GET /tiingo/corporate-actions/{ticker}/distributions", "a ticker's distributions", "Dividends",
             docs=_docs("corporate-actions/dividends")),
        Call("GET /tiingo/corporate-actions/{ticker}/splits", "a ticker's splits", "Splits",
             docs=_docs("corporate-actions/splits")),
        Call("GET /tiingo/utilities/search", "tickers matching a query", "Search", docs=_docs("utilities/search")),
    ),
    verified="2026-11-11",
)

APIS = (TIINGO_REST,)  # the plugin's, its stocks' and its forex's alike (one card: the app draws it once)
