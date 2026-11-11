"""What Tiingo's plugin attaches to (plugin API 2.2, apis.py): one sound card for its stocks and its forex alike, its
calls the ones the plugin really makes (a recording session answers every request; nothing is sent), and nothing asked
to say what it learned (api_facts). With LIMINAL_VENDOR_PAGES=1, every address on the card is asked once: the one test
here that sends anything (the plugins' page check)."""
from __future__ import annotations

import io
import os
import re
import zipfile
from datetime import date, datetime
from types import SimpleNamespace
from urllib.parse import urlparse

import pytest

from liminal_libs.sources import registry
from liminal_libs.sources.apis import dead_links, problems, urls
from liminal_libs.sources.archive import ET
from liminal_libs.sources.http import PublicClient
from plugin_integrator_tiingo import FOREX, TIINGO, BoatsPoller
from plugin_integrator_tiingo.apis import API, APIS, TIINGO_REST, TOKEN
from plugin_integrator_tiingo.client import FILES, SUPPORTED_TICKERS, TiingoFxSource, TiingoSource

from .conftest import FakeResponse

DAY = date(2026, 11, 10)


def _zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("supported_tickers.csv", "ticker,exchange,assetType,priceCurrency,startDate,endDate\n"
                                            "600519,SHG,Stock,CNY,2007-01-04,2026-11-09\n")
    return buf.getvalue()


class Recording:
    """Answers every request (an A-share's record, the supported-tickers file, an empty list otherwise) and records it."""

    def __init__(self):
        self.asked: list[tuple[str, str]] = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.asked.append(("GET", url))
        record = {"ticker": "600519", "exchangeCode": "SHG", "name": "Kweichow Moutai", "startDate": "2007-01-04"}
        resp = FakeResponse(200, record if urlparse(url).path == "/tiingo/daily/600519" else [])
        resp.content = _zip()
        return resp


def _pattern(template: str) -> re.Pattern:
    """A call's path as a pattern: each {placeholder} one path segment."""
    return re.compile("[^/]+".join(re.escape(part) for part in re.split(r"\{[^}]*\}", template)))


def _call_of(method: str, url: str) -> str | None:
    """The card's call a request is (its name), or None: the file by its address, the API's calls by their paths."""
    for call in TIINGO_REST.calls:
        verb, _, target = call.name.partition(" ")
        if verb != method:
            continue
        if target.startswith("https://") and target == url:
            return call.name
        if target.startswith("/") and url.startswith(API + "/") and _pattern(target).fullmatch(urlparse(url).path):
            return call.name
    return None


def _every_request(session: Recording) -> None:
    """Every request the plugin makes, each kind once: the stocks', the forex's, the scan's, the nights'."""
    client = PublicClient(API, headers={"Authorization": "Token K"}, session=session, sleep=lambda s: None)
    files = PublicClient(FILES, session=session, sleep=lambda s: None)
    stocks = TiingoSource(client, has_key=True, listings_on=True, today=DAY, files=files)
    next(stocks.bar_pages("AAPL", DAY, DAY, "day"))
    stocks.instrument("600519.SS")
    stocks.listings("XSHG")
    list(TiingoFxSource(client, has_key=True).bar_pages("C:EURUSD", DAY, DAY, "minute", asset="fx"))
    TIINGO.scan(stocks, today=DAY)
    poller = BoatsPoller(client)
    poller.quotes(["AAPL"])
    night = SimpleNamespace(open=datetime(2026, 11, 10, 20, tzinfo=ET), close=datetime(2026, 11, 11, 4, tzinfo=ET))
    poller.minutes("AAPL", night)


def test_its_card_names_every_call_it_makes_and_none_it_does_not():
    session = Recording()
    _every_request(session)
    assert all(u.startswith((API + "/", FILES + "/")) for _, u in session.asked)  # its two hosts, nothing else
    unnamed = [f"{m} {u}" for m, u in session.asked if _call_of(m, u) is None]
    assert unnamed == []  # every request it made is a call on the card
    made = {_call_of(m, u) for m, u in session.asked}
    assert made == {c.name for c in TIINGO_REST.used}  # and every call the card says it makes, it makes
    assert f"GET {SUPPORTED_TICKERS}" in made and "GET /boats/" in made
    assert {c.name for c in TIINGO_REST.calls if not c.used} >= {"GET /iex", "GET /tiingo/equity/intraday"}


def test_one_sound_card_for_its_stocks_and_its_forex():
    assert APIS == (TIINGO_REST,) and TIINGO.apis is APIS and FOREX.apis is APIS
    assert problems(APIS, today=DAY) == []
    assert TIINGO_REST.docs == "https://www.tiingo.com/documentation/general/overview" and TIINGO_REST.base == API
    assert TIINGO.signup == TOKEN == TIINGO_REST.link("console") == FOREX.signup  # where the token is: its console page
    assert {"docs", "auth", "pricing", "status", "changelog", "console", "terms"} <= {x.kind for x in TIINGO_REST.links}
    parts = {a.name for a in TIINGO_REST.areas}
    assert {"End-of-Day", "IEX", "BOATS Overnight", "24x5 Consolidated", "Forex", "Crypto", "News", "Fundamentals",
            "WebSockets"} <= parts
    assert {a.name for a in TIINGO_REST.covered} >= {"End-of-Day", "Forex", "BOATS Overnight"}
    assert not [c for c in TIINGO_REST.calls if c.writes or c.costs]  # it only reads; nothing on it starts a charge
    assert all(c.area in parts for c in TIINGO_REST.calls)
    assert all(u.startswith("https://") for u in urls(APIS)) and TIINGO_REST.verified == "2026-11-11"
    assert "20,000 an hour" in TIINGO_REST.limits and "50 requests an hour" in TIINGO_REST.limits


def test_it_asks_nothing_to_say_what_it_learned():
    assert TIINGO.api_facts() == {} and FOREX.api_facts() == {}  # the instances hold no run's state
    registry.reload()
    p, fx = registry.providers()["tiingo"], registry.providers()["tiingofx"]
    assert p.apis == APIS == fx.apis and p.interface()["apis"] == ["Tiingo REST API"] == fx.interface()["apis"]


@pytest.mark.skipif(os.environ.get("LIMINAL_VENDOR_PAGES") != "1", reason="asks Tiingo's pages (LIMINAL_VENDOR_PAGES=1)")
def test_every_address_on_its_card_answers():
    assert dead_links(APIS) == []
