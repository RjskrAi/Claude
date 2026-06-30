#!/usr/bin/env python3
"""
QuiverQuant market insights CLI.

Usage:
    python main.py            # broad market overview
    python main.py AAPL       # insights for a specific ticker
"""
import os
import sys

from quiverquant import QuiverQuantClient, market_overview

DEFAULT_API_KEY = "47479dc94bbbfd204c9993077af56d1b16c0d154"


def main():
    api_key = os.environ.get("QUIVER_API_KEY", DEFAULT_API_KEY)
    ticker = sys.argv[1].upper() if len(sys.argv) > 1 else None

    client = QuiverQuantClient(api_key)
    market_overview(client, ticker=ticker)


if __name__ == "__main__":
    main()
