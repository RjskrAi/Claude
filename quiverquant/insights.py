from collections import defaultdict

try:
    from tabulate import tabulate
except ImportError:
    def tabulate(data, headers=(), tablefmt="simple"):
        lines = ["\t".join(str(h) for h in headers)] if headers else []
        for row in data:
            lines.append("\t".join(str(c) for c in row))
        return "\n".join(lines)


def _section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def summarize_congressional(data, top_n=10):
    _section("Congressional Trading")
    if not data:
        print("  No data available.")
        return

    buys, sells = [], []
    for row in data:
        tx = str(row.get("Transaction", "")).lower()
        amount = row.get("Amount") or 0
        try:
            amount = float(str(amount).replace(",", "").replace("$", ""))
        except (ValueError, TypeError):
            amount = 0
        name = row.get("Representative") or row.get("Senator") or "Unknown"
        ticker = row.get("Ticker", "")
        date = row.get("TransactionDate", row.get("Date", ""))
        entry = (name, ticker, f"${amount:,.0f}", date)
        if "purchase" in tx or "buy" in tx:
            buys.append((amount, entry))
        elif "sale" in tx or "sell" in tx:
            sells.append((amount, entry))

    buys.sort(reverse=True)
    sells.sort(reverse=True)

    headers = ["Member", "Ticker", "Amount", "Date"]
    if buys:
        print("\nTop Buys:")
        print(tabulate([e for _, e in buys[:top_n]], headers=headers, tablefmt="rounded_outline"))
    if sells:
        print("\nTop Sells:")
        print(tabulate([e for _, e in sells[:top_n]], headers=headers, tablefmt="rounded_outline"))


def summarize_insider(data, top_n=10):
    _section("Insider Trading")
    if not data:
        print("  No data available.")
        return

    buys, sells = [], []
    for row in data:
        tx = str(row.get("TransactionType", row.get("AcqDisp", ""))).upper()
        shares = row.get("Shares") or 0
        price = row.get("Price") or 0
        try:
            value = float(shares) * float(price)
        except (ValueError, TypeError):
            value = 0
        name = row.get("Name", "Unknown")
        ticker = row.get("Ticker", "")
        date = row.get("Date", "")
        entry = (name, ticker, f"{shares:,.0f}", f"${price}", f"${value:,.0f}", date)
        if tx in ("A", "P", "BUY"):
            buys.append((value, entry))
        elif tx in ("D", "S", "SELL"):
            sells.append((value, entry))

    buys.sort(reverse=True)
    sells.sort(reverse=True)

    headers = ["Insider", "Ticker", "Shares", "Price", "Value", "Date"]
    if buys:
        print("\nTop Insider Buys:")
        print(tabulate([e for _, e in buys[:top_n]], headers=headers, tablefmt="rounded_outline"))
    if sells:
        print("\nTop Insider Sells:")
        print(tabulate([e for _, e in sells[:top_n]], headers=headers, tablefmt="rounded_outline"))


def summarize_wallstreetbets(data, top_n=15):
    _section("WallStreetBets Sentiment")
    if not data:
        print("  No data available.")
        return

    rows = []
    for row in data:
        ticker = row.get("Ticker", "")
        mentions = row.get("Mentions", row.get("Count", 0))
        sentiment = row.get("Sentiment", row.get("Sentiment_Score", "N/A"))
        rank = row.get("Rank", "")
        try:
            sentiment = f"{float(sentiment):.2f}"
        except (ValueError, TypeError):
            pass
        rows.append((rank, ticker, mentions, sentiment))

    rows.sort(key=lambda x: x[2] if isinstance(x[2], int) else 0, reverse=True)
    print(tabulate(rows[:top_n], headers=["Rank", "Ticker", "Mentions", "Sentiment"], tablefmt="rounded_outline"))


def summarize_offexchange(data, top_n=10):
    _section("Off-Exchange / Dark Pool Activity")
    if not data:
        print("  No data available.")
        return

    rows = []
    for row in data:
        ticker = row.get("Ticker", "")
        pct = row.get("OffExchangeVol") or row.get("DarkPoolPercent") or 0
        volume = row.get("TotalVolume") or row.get("Volume") or 0
        date = row.get("Date", "")
        try:
            pct = float(pct)
        except (ValueError, TypeError):
            pct = 0
        rows.append((pct, ticker, f"{pct:.1f}%", f"{volume:,}" if isinstance(volume, (int, float)) else volume, date))

    rows.sort(reverse=True)
    print(tabulate(
        [(t, p, v, d) for _, t, p, v, d in rows[:top_n]],
        headers=["Ticker", "Dark Pool %", "Volume", "Date"],
        tablefmt="rounded_outline"
    ))


def summarize_govcontracts(data, top_n=10):
    _section("Government Contracts")
    if not data:
        print("  No data available.")
        return

    rows = []
    for row in data:
        ticker = row.get("Ticker", "")
        amount = row.get("Amount") or 0
        agency = row.get("Agency", "")
        description = str(row.get("Description", ""))[:50]
        date = row.get("Date", "")
        try:
            amount = float(str(amount).replace(",", "").replace("$", ""))
        except (ValueError, TypeError):
            amount = 0
        rows.append((amount, ticker, f"${amount:,.0f}", agency, description, date))

    rows.sort(reverse=True)
    print(tabulate(
        [(t, a, ag, d, dt) for _, t, a, ag, d, dt in rows[:top_n]],
        headers=["Ticker", "Amount", "Agency", "Description", "Date"],
        tablefmt="rounded_outline"
    ))


def market_overview(client, ticker=None):
    label = ticker if ticker else "Broad Market"
    print(f"\n{'#'*60}")
    print(f"  QuiverQuant Market Insights — {label}")
    print(f"{'#'*60}")

    endpoints = [
        ("Congressional Trading", client.get_congressional_trading, summarize_congressional),
        ("Insider Trading", client.get_insider_trading, summarize_insider),
        ("WallStreetBets", client.get_wallstreetbets, summarize_wallstreetbets),
        ("Off-Exchange", client.get_offexchange, summarize_offexchange),
        ("Gov Contracts", client.get_government_contracts, summarize_govcontracts),
    ]

    for name, fetch_fn, summarize_fn in endpoints:
        try:
            data = fetch_fn(ticker) if ticker else fetch_fn()
            summarize_fn(data)
        except Exception as exc:
            print(f"\n[{name}] Error: {exc}")

    print(f"\n{'#'*60}\n")
