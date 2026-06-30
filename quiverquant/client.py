import requests

BASE_URL = "https://api.quiverquant.com/beta"


class QuiverQuantClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {api_key}"})

    def _get(self, path):
        url = f"{BASE_URL}{path}"
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_congressional_trading(self, ticker=None):
        path = f"/live/congresstrading/{ticker}" if ticker else "/live/congresstrading"
        return self._get(path)

    def get_senate_trading(self, ticker=None):
        path = f"/live/senatetrading/{ticker}" if ticker else "/live/senatetrading"
        return self._get(path)

    def get_house_trading(self, ticker=None):
        path = f"/live/housetrading/{ticker}" if ticker else "/live/housetrading"
        return self._get(path)

    def get_insider_trading(self, ticker=None):
        path = f"/live/insiders/{ticker}" if ticker else "/live/insiders"
        return self._get(path)

    def get_lobbying(self, ticker=None):
        path = f"/live/lobbying/{ticker}" if ticker else "/live/lobbying"
        return self._get(path)

    def get_government_contracts(self, ticker=None):
        path = f"/live/govcontracts/{ticker}" if ticker else "/live/govcontracts"
        return self._get(path)

    def get_wallstreetbets(self, ticker=None):
        path = f"/live/wallstreetbets/{ticker}" if ticker else "/live/wallstreetbets"
        return self._get(path)

    def get_twitter_sentiment(self, ticker):
        return self._get(f"/live/twitter/{ticker}")

    def get_offexchange(self, ticker=None):
        path = f"/live/offexchange/{ticker}" if ticker else "/live/offexchange"
        return self._get(path)
