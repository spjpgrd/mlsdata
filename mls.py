import urllib2
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse

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

def gather_facts(team):
    print 'Gathering facts for ' + team.name + '...'
    for year in team.yearsActive:
        print 'Collecting ' + str(year) + ' match facts...'
        url_to_scrape = team.website + '/schedule?month=all&year=' + str(year)
        page = urllib2.urlopen(url_to_scrape)
        soup = BeautifulSoup(page, 'html.parser')
        matches = soup.find_all('article', class_='match_item')
        for match in matches:
            homeAway = match.find('span', class_='match_home_away').string
            matchOpponent = match.find('img', class_='club_logo')['title']
            matchDate = match.find('div', class_='match_date')
            matchTime = matchDate.find('span', class_='match_time').string
            matchDateAndTime = matchDate.contents[0] + matchTime
            parsedDate = parse(matchDateAndTime)
            matchLocation = match.find('div', class_='match_location_short').string
            matchType = match.find('span', class_='match_competition').string
            matchResultField = match.find('span', class_='match_result')
            matchResult = MatchResult(None, None, 'SCHEDULED')
            if matchResultField is not None:
                matchResultString = matchResultField.string
                scores = re.findall(r'\d', matchResultString)
                if len(scores) < 1:
                    scores.append(u'-1')
                    scores.append(u'-1')
                if 'WIN' in matchResultString:
                    matchResult = MatchResult(scores[0], scores[1], 'WIN')
                elif 'LOSS' in matchResultString:
                    matchResult = MatchResult(scores[0], scores[1], 'LOSS')
                elif 'DRAW' in matchResultString:
                    matchResult = MatchResult(scores[0], scores[1], 'DRAW')
                else:
                    matchResult = MatchResult(scores[0], scores[1], 'UNKNOWN')
            m = Match(matchLocation, parsedDate, matchType, matchOpponent, homeAway, matchResult)
            team.addMatch(m)
        print 'Collecting ' + str(year) + ' match facts... COMPLETE'

crew = Team("Columbus Crew", "https://www.columbuscrewsc.com", [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017])
# crew = Team("Columbus Crew (TESTING)", "https://www.columbuscrewsc.com", [2010])
gather_facts(crew)

for year in crew.yearsActive:
    print str(year) + ' record: %s' % (crew.team_record(year, None))
