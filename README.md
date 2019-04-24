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

Results after game 140 TCEC 15 Division P:

|Engine                 |Rating|1      |2      |3      |4      |5      |6      |7      |8      |
|-----------------------|------|-------|-------|-------|-------|-------|-------|-------|-------|
|Stockfish 19040612     |3200  |97.0900|02.9100|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|LCZero v0.21.1-n41800  |3200  |02.9100|97.0700|00.0200|00.0000|00.0000|00.0000|00.0000|00.0000|
|Komodo 2306.00         |3089  |00.0000|00.0100|74.5500|19.9200|04.3700|01.1500|00.0000|00.0000|
|AllieStein v0.3dev-n6.1|3079  |00.0000|00.0100|19.6100|59.9700|16.7300|03.6700|00.0100|00.0000|
|Houdini 6.03           |3100  |00.0000|00.0000|04.1000|12.9000|42.4000|40.3500|00.2500|00.0000|
|KomodoMCTS 2306.00     |3059  |00.0000|00.0000|01.7200|07.2100|36.4700|54.2000|00.3800|00.0200|
|Fire 011819            |3000  |00.0000|00.0000|00.0000|00.0000|00.0300|00.5000|68.1500|31.3200|
|Ethereal 11.38         |2976  |00.0000|00.0000|00.0000|00.0000|00.0000|00.1300|31.2100|68.6600|

