import random
from options import options
from progressbar import ProgressBar, Percentage, Bar, ETA

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