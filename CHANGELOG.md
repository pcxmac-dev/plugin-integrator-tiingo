# Changelog

## 0.3.0 (2026-11-11)

Its API on its page (plugin API 2.2, liminal-libs 1.49.0; the user: "each plugin should reflect the the API its
attached to, and present links that provide documentation, the plugin interface should more or less contain what it
already has, BUT, it should also expose more of what the API is about"). Both feeds declare one card (`apis`, from
`apis.py`: `TIINGO_REST`, set on `TiingoFeed`), Tiingo's REST API as Tiingo's pages said on 2026-11-11: what it is
and for, its address, the token's form, its plans' limits (Starter 50 requests an hour and 1,000 a day, Power 10,000
and 100,000, Commercial 20,000 and 150,000, with their symbols and bandwidth a month) and prices, and Tiingo's pages
(the documentation, connecting, symbology, pricing, the status and uptime pages, the changelog, the API token page,
the terms). Its 13 parts, the documentation's sections with the WebSockets, say what is used here (7) and what is
not; its 25 calls the 10 made here (the supported-tickers file among them), each with what for, beside the notable
others. `signup` is the API token page's address (a link on the Plugins view). `api_facts` says nothing (the
contract's): the plugin holds no run's state. Tiingo's site answers any address under its documentation with a page,
so each page on the card was read, not only asked for. Tests: the card names every call the plugin makes and none it
does not; every address on it answers (with `LIMINAL_VENDOR_PAGES=1`). Nothing it fetches changed. Requires
liminal-libs 1.49.0.

## 0.2.0 (2026-11-03)

Renamed `plugin-integrator-tiingo` (the package `plugin_integrator_tiingo`; it was `liminal-plugin-tiingo`) on 2026-11-03: the naming by system (plugins are `plugin-<app>-<name>`), on liminal-libs 1.4.0 (`liminal_libs`, the library renamed with it).

Classes on plugin API 2.0 (liminal-libs 1.3.0; the user: "all the plugins under liminal should basically
follow inheritance/oop paradigm"), versioned 0.2.0 with Liminal's release (every distribution at 0.2.0 on
a `release/0.2.0` branch). The two feeds are `TiingoPlugin` (`TIINGO`) and `TiingoForex` (`FOREX`, the
part: `part_of`), both `TiingoFeed`, the base holding what they declare and do alike (the key, `view`,
`rate`, `has_keys`, and `client`: the client on the key, its window and day cap held under Tiingo's name
for both); what each declares is a class attribute of the record field's name, what it does a method of
the callback's (the stocks' `build`, `reporter`, `markets`, `scan`, Blue Ocean's nights a `live` property
polled by `night_poller`; the forex's `view` (once `view_forex`: the base's, with the currencies'
history), `build` (once `build_forex`), `markets`). The forex declares its publication delay itself
(`TiingoForex.delays`: the tiingofx row the library's `freshness.py` held). Nothing they do changed: the
same requests, plans, scan, strings and limits.

## 1.5.1 (2026-11-03)

`TIINGO_LISTINGS` has its choices (off, on) in the record, so the app's Plugins view offers it beside the plan.

## 1.5.0 (2026-11-02)

Shanghai's and Shenzhen's A-shares (the user: "update existing plugins, add exchanges where applicable and
symbols"): the stocks feed carries them (plugin API 1.12, `Provider.exchanges`: every US listing, XSHG and XSHE),
stored as `600519.SS` and `000001.SZ` (the library's notation) and asked for by their bare codes, Tiingo's form
(`/tiingo/daily/600519`, from 2007-01-04). A listing's record names it and its exchange (`instrument`); the
exchanges come by name (`exchanges`); with `TIINGO_LISTINGS=on` the A-shares are listed in the directory from
Tiingo's supported-tickers file (about 10 MB, at each directory refresh while on). Requires liminal-libs 1.2.0.

## 1.4.1 (2026-11-02)

The plugin imports the library as `liminal_libs` and depends on liminal-libs (the app, renamed liminal-charts, is no longer needed to run the tests; the user, 2026-11-02: "lets rename the app to liminal-charts").

## 1.4.0 (2026-11-01)

- Released as its own package, `plugin-integrator-tiingo`, registered under the entry point group
  `liminal.providers` (a module of two feeds: `tiingo`, `tiingofx`); its version is the distribution's.
- Its free plan and caps are in it (`TIER`, `PER_RUN`, `PER_DAY`), no longer in the app's
  `config.PUBLIC_FEEDS`; its key is read from the settings' plugin variables (`Settings.env`), no
  longer from a field of the app's settings.
- Plugin API 1.10: the machine-wide symbol ledger and the session calendar (Blue Ocean's nights)
  are reached through the contract (`liminal.sources.registry.MachineLedger`,
  `liminal.sources.stream.session_at`).

## 1.3.0 (2026-10-31)

- Built into the app (then massive-collate): its live Blue Ocean nights and its client in its
  module (plugin API 1.6).

## 1.2.0 and before

- Built into the app (then massive-collate); see the app's history.
