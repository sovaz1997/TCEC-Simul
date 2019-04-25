from urllib.request import urlopen

import json
import copy
import numpy
import os.path
import math
import sys
import csv

from progressbar import ProgressBar, Percentage, Bar, ETA
from options import options
from score import Score
from engine import Engine
from game import Game

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
                elif crosstable[i][j][k] == 0.5:
                    scores[i].score += 0.5
    
    for i in range(crosstable.shape[0]):
        for j in range(crosstable.shape[1]):
            for k in range(crosstable.shape[2]):
                if crosstable[i][j][k] == 1:
                    scores[i].SB += scores[j].score
                    
                    if scores[i].score == scores[j].score:
                        scores[i].directEncounter += 1

                elif scores[i] == 0.5:
                    scores[i].SB += scores[j].score / 2
                    
                    if scores[i].score == scores[j].score:
                        scores[i].directEncounter += 0.5
    result = []

    for i in sorted(scores):
        result.append(i.engine_name)

    return result, scores

def makeSimulations(games, engines, cnt, playedCount):
    result = {}
    avg_scores = {}

    for i in engines:
        result[i] = numpy.zeros(len(engines))
    
    progress, progress_maxval = 0, cnt
    pbar = ProgressBar(widgets=['Simulation processing: ', Percentage(), Bar(), ' ', ETA(), ], maxval=progress_maxval).start()

    roundSize = (len(engines) * len(engines) - len(engines)) / 2
    crosstable = numpy.zeros((len(engines), len(engines), int(len(games) / roundSize)), dtype=float)

    for i in range(cnt):
        for j in range(playedCount + 1, len(games)):
            games[j].simulate()

        positions, scores = calculatePositions(engines, games, crosstable, roundSize)
        
        for j in range(len(positions)):
            result[positions[j]][j] += 1

        for j in scores:
            if not j.engine_name in avg_scores:
                avg_scores[j.engine_name] = 0
            avg_scores[j.engine_name] +=  j.score

        progress += 1
        pbar.update(progress)
    table = []
    engines_table = []
    engines_ratings = []
    
    print('\n')

    print("{:<30}".format('Engine') + ": ", end=' ')
    print("{:<7}".format('Scores'), end=' ')

    for i in range(1, len(engines) + 1):
        print("{:<7}".format(str(i)), end=' ')
    print('')

    for i in avg_scores:
        avg_scores[i] /= cnt

    for i in sorted(result, key=lambda x: avg_scores[x], reverse=True):
        engines_table.append(i)
        engines_ratings.append(engines[i].engine_elo)
        row = []
        print("{:<30}".format(i) + ": ", end=' ')
        print("{:07.4f}".format(avg_scores[i]), end = ' ')
        for j in result[i]:
            val = j / cnt * 100
            writed_val = "{:07.4f}".format(val)
            print(writed_val, end=' ')
            row.append(writed_val)
        table.append(row)
        print('')
    
    if options.csv_export:
        saveToCSV(engines_table, engines_ratings, table, avg_scores)

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

def saveToCSV(engines, ratings, table, avg_scores):
    with open(options.csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(['Engine', 'Rating', 'Avg. Scores'] + [i for i in range(1, len(engines) + 1)])

        for i in range(len(engines)):
            writer.writerow([engines[i], ratings[i], avg_scores[engines[i]]] + table[i])

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