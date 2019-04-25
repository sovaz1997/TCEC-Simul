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