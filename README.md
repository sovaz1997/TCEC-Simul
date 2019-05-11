# TCEC-Simul

TCEC Simulation (predict results)

The program generates a table with a TCEC tournament prediction: engines and probabilities of place, BayesElo system.

## Installation

+ download Python 3 from here: https://www.python.org/
+ go to folder with program and run command for install requirements:
  ```
  pip3 install -r requirements.txt
  ```



## Usage
python tcecsimul.py [params]

Params description (-h):
```
-h - show help
-eA <val> - set elo advantage
-eD <val> - set elo draw
-l <val> - link to JSON schedule
-r <val> - local file with engine ratings
-s <val> - number of simulations
-e <val> - export results to CSV-table
```
## Example
You want to simulate the results of the current TCEC tournament with an accuracy of 10K simulations. You will use the ratings from your json file "TCEC-SuFi-S15.json" for TCEC S15 Superfinal and export the results to a table "results.csv".

```
python .\tcecsimul.py -s 10000 -e results.csv -r TCEC-SuFi-S15.json
```

Results after game 3 TCEC S15 Superfinal Division:


|Engine|Rating                       |Avg. Scores|1                                            |2      |
|------|-----------------------------|-----------|---------------------------------------------|-------|
|LCZero v0.21.1-nT40.T8.610|3450                         |52.95195   |90.7700                                      |09.2300|
|Stockfish 19050918|3400                         |47.04805   |09.2300                                      |90.7700|






