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

Results after game 151 TCEC 15 Division P:


|Engine                        |Rating                                                                   |Avg. Scores|1  |2  |3      |4      |5      |6      |7      |8      |
|------------------------------|-------------------------------------------------------------------------|-----------|---|---|-------|-------|-------|-------|-------|-------|
|Stockfish 19040612            |3200                                                                     |27.76755   |99.7100|00.2900|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|LCZero v0.21.1-n41800         |3200                                                                     |25.2685    |00.2900|99.7100|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|Komodo 2306.00                |3089                                                                     |21.4976    |00.0000|00.0000|87.6400|09.3900|02.9100|00.0600|00.0000|00.0000|
|AllieStein v0.3dev-n6.1       |3079                                                                     |20.48405   |00.0000|00.0000|09.8000|75.9600|11.6100|02.6300|00.0000|00.0000|
|Houdini 6.03                  |3100                                                                     |19.9113    |00.0000|00.0000|02.5400|10.7700|67.8200|18.8300|00.0400|00.0000|
|KomodoMCTS 2306.00            |3059                                                                     |19.545     |00.0000|00.0000|00.0200|03.8800|17.6600|78.0800|00.3600|00.0000|
|Ethereal 11.38                |2976                                                                     |17.2283    |00.0000|00.0000|00.0000|00.0000|00.0000|00.4000|84.7400|14.8600|
|Fire 011819                   |3000                                                                     |16.2977    |00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|14.8600|85.1400|



