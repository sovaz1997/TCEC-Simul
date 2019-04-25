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