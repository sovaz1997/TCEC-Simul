from urllib.request import urlopen
import json
import random
import copy
import numpy
import os.path
import math
import sys
from progressbar import ProgressBar, Percentage, Bar, ETA
import csv

class Options:
        def __init__(self, eloAdvantage=32.8, eloDraw=350, JSONLink='https://tcec.chessdom.com/schedule.json', engines_file_name='engines.json', simulcount=10000, csv_filename='table.csv', csv_export=False):
            self.eloAdvantage = eloAdvantage
            self.eloDraw = eloDraw
            self.JSONLink = JSONLink
            self.engines_file_name = engines_file_name
            self.simulcount = simulcount
            self.csv_filename = csv_filename
            self.csv_export = csv_export

options = Options()

class Score:
    def __init__(self):
        self.score = 0
        self.SB = 0
        self.numOfWins = 0
        self.directEncounter = 0
        self.engine_name = ''
        self.disconnect_count = 0
    
    def __lt__(self, other):
        #Tiebreaks

        #0. Score
        if self.score > other.score:
            return True
        elif self.score < other.score:
            return False
        
        #1. Disconnect count
        if self.disconnect_count < other.disconnect_count:
            return True
        elif self.disconnect_count > other.disconnect_count:
            return False

        #2. Direct encounter
        if self.directEncounter > other.directEncounter:
            return True
        elif self.directEncounter < other.directEncounter:
            return False
        
        #3. Number of wins
        if self.numOfWins > other.numOfWins:
            return True
        elif self.numOfWins < other.numOfWins:
            return False

        #4. SB
        if self.SB > other.SB:
            return True
        elif self.SB < other.SB:
            return False
        
        return True

class Engine:
    def __init__(self, engine_name, engine_elo, id):
        self.engine_name = engine_name
        self.engine_elo = engine_elo
        self.id = id
    
    def __str__(self):
        return (self.engine_name + ': ' + str(self.engine_elo))

class Game:
    def __init__(self, white_engine, black_engine, result=0, played=0, disconnect=-1):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.result = result
        self.played = played
        self.disconnect = disconnect
    
    def simulate(self):
        goodness = 1000000000
        res = random.randint(0, goodness)

        whiteWin = self.whiteProbability()
        blackWin = self.blackProbability()

        if res <= goodness * whiteWin:
            self.result = 1
        elif res <= goodness * (whiteWin + blackWin):
            self.result = 0
        else:
            self.result = 0.5

        self.played = True
    
    def clearResult(self):
        self.played = False
    
    def function(self, delta):
        return 1 / (1 + 10 ** (delta / 400))
    
    def whiteProbability(self):
        return self.function(self.black_engine.engine_elo - self.white_engine.engine_elo - options.eloAdvantage + options.eloDraw)
    
    def blackProbability(self):
        return self.function(self.white_engine.engine_elo - self.black_engine.engine_elo + options.eloAdvantage + options.eloDraw)

    def __str__(self):
        res = str(self.white_engine) + '\n' + str(self.black_engine)
        if self.played:
            res += '\n' + str(self.result)
        
        return res

def getSchedule(link):
    url = link
    response = urlopen(url)
    string = response.read().decode('utf-8')
    return string

def simulate(games):
    for i in games:
        i.simulate()

def calculatePositions(engines, games, crosstable, roundSize):
    scores = [Score() for i in range(len(engines))]

    cnt_engines = len(engines)

    index = 0
    for i in engines:
        scores[index].engine_name = i
        index += 1

    gameNumber = 0

    for i in games:
        crosstable[i.white_engine.id, i.black_engine.id, int(gameNumber // roundSize)] = i.result
        crosstable[i.black_engine.id, i.white_engine.id, int(gameNumber // roundSize)] = 1 - i.result
        gameNumber += 1
        if i.disconnect == 0:
            scores[i.white_engine.id].disconnect_count += 1 
        elif i.disconnect == 1:
            scores[i.black_engine.id].disconnect_count += 1   

    for i in range(crosstable.shape[0]):
        for j in range(crosstable.shape[1]):
            for k in range(crosstable.shape[2]):
                if crosstable[i][j][k] == 1:
                    scores[i].score += 1
                    scores[i].numOfWins += 1

                elif crosstable[i][j][k] == 0:
                    scores[j].score += 1
                    scores[j].numOfWins += 1
                else:
                    scores[i].score += 0.5
                    scores[j].score += 0.5
    
    for i in range(crosstable.shape[0]):
        for j in range(crosstable.shape[1]):
            for k in range(crosstable.shape[2]):
                if crosstable[i][j][k] == 1:
                    scores[i].SB += scores[j].score
                    
                    if scores[i].score == scores[j].score:
                        scores[i].directEncounter += 1

                elif crosstable[i][j][k] == 0:
                    scores[j].SB += scores[i].score
                    
                    if scores[i].score == scores[j].score:
                        scores[j].directEncounter += 1
                else:
                    scores[i].SB += scores[j].score / 2
                    scores[j].SB += scores[i].score / 2
                    
                    if scores[i].score == scores[j].score:
                        scores[i].directEncounter += 0.5
                        scores[j].directEncounter += 0.5

    result = []

    for i in sorted(scores):
        result.append(i.engine_name)

    return result

def makeSimulations(games, engines, cnt, playedCount):
    result = {}

    for i in engines:
        result[i] = numpy.zeros(len(engines))
    
    progress, progress_maxval = 0, cnt
    pbar = ProgressBar(widgets=['Simulation processing: ', Percentage(), Bar(), ' ', ETA(), ], maxval=progress_maxval).start()

    roundSize = (len(engines) * len(engines) - len(engines)) / 2
    crosstable = numpy.zeros((len(engines), len(engines), int(len(games) / roundSize)), dtype=float)

    for i in range(cnt):
        for j in range(playedCount + 1, len(games)):
            games[j].simulate()

        positions = calculatePositions(engines, games, crosstable, roundSize)
        
        for j in range(len(positions)):
            result[positions[j]][j] += 1
        progress += 1
        pbar.update(progress)
    table = []
    engines_table = []
    engines_ratings = []
    
    for i in sorted(result, key=lambda x: result[x].argmax()):
        engines_table.append(i)
        engines_ratings.append(engines[i].engine_elo)
        row = []
        print("{:<30}".format(i) + ": ", end=' ')
        for j in result[i]:
            val = j / cnt * 100
            writed_val = "{:07.4f}".format(val)
            print(writed_val, end=' ')
            row.append(writed_val)
        table.append(row)
        print('')
    
    if options.csv_export:
        saveToCSV(engines_table, engines_ratings, table)

def setEnginesInfo(engine_names, filename):
    data = {}

    print('Input engine ratings:')
    
    for i in engine_names:
        print(i + ": ", end='')
        rating = int(input())
        data[i] = rating
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def installRatingEngines(engine_names, filename):
    engines = {}

    with open(filename, 'r') as data_file:
        data = json.load(data_file)

    id = 0
    for i in data:
        engines[i] = Engine(i, data[i], id)
        id += 1

    return engines

def saveToCSV(engines, ratings, table):
    with open(options.csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(['Engine', 'Rating'] + [i for i in range(1, len(engines) + 1)])

        for i in range(len(engines)):
            writer.writerow([engines[i], ratings[i]] + table[i])

fromFile = False

for i in range(len(sys.argv)):
    if sys.argv[i] == '-eA':
        options.eloAdvantage = int(sys.argv[i+1])
    elif sys.argv[i] == '-eD':
        options.eloDraw = int(sys.argv[i+1])
    elif sys.argv[i] == '-l':
        options.JSONLink = sys.argv[i+1]
    elif sys.argv[i] == '-r':
        fromFile = True
        options.engines_file_name = sys.argv[i+1]
    elif sys.argv[i] == '-s':
        options.simulcount = int(sys.argv[i+1])
    elif sys.argv[i] == '-e':
        options.csv_export = True
        options.csv_filename = sys.argv[i+1]
    elif sys.argv[i] == '-h':
        print('-h - show help', '-eA <val> - set elo advantage',\
        '-eD <val> - set elo draw', '-l <val> - link to JSON schedule',\
        '-r <val> - local file with engine ratings', '-s <val> - number of simulations',\
        '-e <val> - export results to CSV-table', sep='\n')
        exit(0)

schedule = json.loads(getSchedule(options.JSONLink))
engines_names = set()

# Find endines in file
for i in schedule:
    engines_names.add(i['White'])
    engines_names.add(i['Black'])

# Connect engines with ratings from file
if not os.path.isfile(options.engines_file_name) or not fromFile:
    setEnginesInfo(engines_names, options.engines_file_name)
    print('Saved to', options.engines_file_name)

engines = installRatingEngines(engines_names, options.engines_file_name)

print('Engines:')
for i in engines:
    print(engines[i])
print('')

games = []

playedCount = 0

for i in schedule:
    if not 'Result' in i:
        games.append(Game(engines[i['White']], engines[i['Black']]))
    else:
        crash_state = -1

        if i['Result'] != '*':
            playedCount += 1
            if i['Termination'] == 'White disconnects':
                crash_state = 0
            elif i['Termination'] == 'Black disconnects':
                crash_state = 1

        if i['Result'] == '1-0':
            games.append(Game(engines[i['White']], engines[i['Black']], 1, 1, crash_state))
        elif i['Result'] == '0-1':
            games.append(Game(engines[i['White']], engines[i['Black']], 0, 1, crash_state))
        elif i['Result'] == '1/2-1/2':
            games.append(Game(engines[i['White']], engines[i['Black']], 0.5, 1, crash_state))
        else:
            games.append(Game(engines[i['White']], engines[i['Black']], 0, 0))

print('Played: {}/{}\n'.format(playedCount, len(games)))
makeSimulations(games, engines, options.simulcount, playedCount)