from urllib.request import urlopen
import json
import random

eloAdvantage = 32.8
eloDraw = 97.3

class Engine:
    def __init__(self, engine_name, engine_elo):
        self.engine_name = engine_name
        self.engine_elo = engine_elo
    
    def __str__(self):
        return self.engine_name + ': ' + str(self.engine_elo)

class Game:
    def __init__(self, white_engine, black_engine, result=0, played=0):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.result = result
        self.played = played
    
    def simulate():
        if not self.played:
            goodness = 1000000000
            res = random.randint(0, goodness)

            whiteWin = whiteProbability()
            blackWin = blackProbability()

            if res <= goodness * whiteWin:
                self.result = 1
            elif res <= goodness * blackWin:
                self.result = 0
            else:
                self.result = 0.5

            self.played = True
    
    def clearResult(self):
        self.played = False
    
    def function(delta):
        return 1 / (1 + 10 ** (delta / 400))
    
    def whiteProbability(self):
        return f(self.black_engine.engine_elo - self.white_engine.white_elo - eloAdvantage + eloDraw)
    
    def blackProbability(self):
        return f(self.white_engine.engine_elo - self.black_engine.white_elo + eloAdvantage + eloDraw)

    def __str__(self):
        res = str(self.white_engine) + '\n' + str(self.black_engine)
        if self.played:
            res += '\n' + str(self.result)
        
        return res

def getSchedule():
    url = 'https://tcec.chessdom.com/schedule.json'
    response = urlopen(url)
    string = response.read().decode('utf-8')
    return string

def simulate(games):
    for i in games:
        i.simulate()

def calculatePositions(games):
    scores = {}

    for i in games:
        if i.played
            if not i.white_engine.engine_name in result:
                scores[i.white_engine.engine_name] = 0

            if i.result == 1:
                scores[i.white_engine.engine_name] += 1
            elif i.result == 0:
                scores[i.black_engine.engine_name] += 1
            else:
                scores[i.white_engine.engine_name] += 0.5
                scores[i.black_engine.engine_name] += 0.5



schedule = json.loads(getSchedule()) # получение расписания
engines_names = set()

# Поиск движков в файле
for i in schedule:
    engines_names.add(i['White'])
    engines_names.add(i['Black'])


engines = {}

# Сопоставления движка и его рейтинга
for i in engines_names:
    engines[i] = Engine(i, 2500)

for i in engines:
    print(i)

games = [] # список всех игр

for i in schedule:
    if not 'Result' in i:
        games.append(Game(engines[i['White']], engines[i['Black']]))
    else:
        if i['Result'] == '1-0':
            games.append(Game(i['White'], i['Black'], 1, 1))
        elif i['Result'] == '0-1':
            games.append(Game(i['White'], i['Black'], 0, 1))
        else:
            games.append(Game(i['White'], i['Black'], 0.5, 1))


