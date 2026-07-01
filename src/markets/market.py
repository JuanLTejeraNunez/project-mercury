class Market:
    def __init__(self, source, market_id, league, season, home, away, notes):
        self.source = source
        self.market_id = market_id
        self.league = league
        self.season = season
        self.home = home
        self.away = away
        self.notes = notes

    def __repr__(self):
        return f"<Market {self.source}:{self.market_id} {self.league}>"

