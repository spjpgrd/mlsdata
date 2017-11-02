class Team:
    def __init__(self, name, website, yearsActive):
        self.name = name
        self.website = website
        self.yearsActive = yearsActive
        self.matches = []
    def addMatch(self, match):
        self.matches.append(match)
    def team_record(self, season, type):
        if season is None:
            season = self.yearsActive[0]
        winCount = 0
        drawCount = 0
        lossCount = 0
        scheCount = 0
        for match in self.matches:
            if match.season == season:
                if type is not None:
                    if match.type == type:
                        if "WIN" in match.result.type:
                            winCount += 1
                        elif "LOSS" in match.result.type:
                            lossCount += 1
                        elif "DRAW" in match.result.type:
                            drawCount += 1
                        else:
                            scheCount += 1
                else:
                    if "WIN" in match.result.type:
                        winCount += 1
                    elif "LOSS" in match.result.type:
                        lossCount += 1
                    elif "DRAW" in match.result.type:
                        drawCount += 1
                    else:
                        scheCount += 1
        return "%i-%i-%i" % (winCount, drawCount, lossCount)
