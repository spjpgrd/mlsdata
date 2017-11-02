class Match:
    def __init__(self, location, date, type, opponent, homeOrAway, result):
        self.location = location
        self.date = date
        self.season = date.year
        self.type = type
        self.opponent = opponent
        self.homeOrAway = homeOrAway
        self.result = result
    def __repr__(self):
        return "<Match season:%i opponent:%s result:%s>" % (self.season, self.opponent, self.result)
    def __str__(self):
        hoa = "@"
        if self.homeOrAway == "H":
            hoa = "vs"
        return "%s Game: %s %s %s | %s" % (self.type, self.date, hoa, self.opponent, self.result)

class MatchResult:
    def __init__(self, winnerScore, loserScore, type):
        self.winner_score = winnerScore
        self.loser_score = loserScore
        self.type = type
