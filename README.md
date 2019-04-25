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
You want to simulate the results of the current TCEC tournament with an accuracy of 10K simulations. You will use the ratings from your json file "divP.json" for TCEC Division P and export the results to a table "results.csv".

```
python tcecsimul.py -s 10000 -r divP.json -e results.csv
```

Results after game 144 TCEC 15 Division P:

|Engine|Rating                       |Avg. Scores|1                                            |2      |3      |4      |5      |6      |7      |8      |
|------|-----------------------------|-----------|---------------------------------------------|-------|-------|-------|-------|-------|-------|-------|
|Stockfish 19040612|3200                         |27.87835   |99.7800                                      |00.2200|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|LCZero v0.21.1-n41800|3200                         |24.9754    |00.2200                                      |99.7700|00.0100|00.0000|00.0000|00.0000|00.0000|00.0000|
|Komodo 2306.00|3089                         |21.08125   |00.0000                                      |00.0100|49.9900|25.8500|20.4000|03.7500|00.0000|00.0000|
|AllieStein v0.3dev-n6.1|3079                         |20.89365   |00.0000                                      |00.0000|33.3100|42.4700|18.9000|05.3200|00.0000|00.0000|
|Houdini 6.03|3100                         |20.4955    |00.0000                                      |00.0000|15.1100|26.2000|43.1200|15.5700|00.0000|00.0000|
|KomodoMCTS 2306.00|3059                         |19.93895   |00.0000                                      |00.0000|01.5800|05.4800|17.5800|75.3200|00.0400|00.0000|
|Fire 011819|3000                         |16.6185    |00.0000                                      |00.0000|00.0000|00.0000|00.0000|00.0300|74.3100|25.6600|
|Ethereal 11.38|2976                         |16.1184    |00.0000                                      |00.0000|00.0000|00.0000|00.0000|00.0100|25.6500|74.3400|


