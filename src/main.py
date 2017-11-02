import urllib2
import re
from team import Team
from match import Match, MatchResult
from bs4 import BeautifulSoup
from dateutil.parser import parse

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
