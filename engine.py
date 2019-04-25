class Engine:
    def __init__(self, engine_name, engine_elo, id):
        self.engine_name = engine_name
        self.engine_elo = engine_elo
        self.id = id
    
    def __str__(self):
        return (self.engine_name + ': ' + str(self.engine_elo))