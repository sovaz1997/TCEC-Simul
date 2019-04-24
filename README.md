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
You want to simulate the results of the current TCEC tournament with an accuracy of 100 000 simulations. You will use the ratings from your json file "divP.json" for TCEC Division P and export the results to a table "results.csv".

Results after game 136 TCEC 15 Division P:

|Engine|Rating                       |1     |2      |3      |4      |5      |6      |7      |8      |
|------|-----------------------------|------|-------|-------|-------|-------|-------|-------|-------|
|Stockfish 19040612|3200                         |99.9780|00.0220|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|LCZero v0.21.1-n41800|3200                         |00.0220|99.6390|00.3380|00.0010|00.0000|00.0000|00.0000|00.0000|
|Komodo 2306.00|3089                         |00.0000|00.3380|82.7150|12.6220|03.5270|00.7970|00.0010|00.0000|
|AllieStein v0.3dev-n6.1|3079                         |00.0000|00.0010|08.6800|34.2660|34.3600|22.3290|00.3640|00.0000|
|KomodoMCTS 2306.00|3059                         |00.0000|00.0000|02.7050|22.8430|31.3970|42.1720|00.8800|00.0030|
|Houdini 6.03|3100                         |00.0000|00.0000|05.5620|30.2300|30.4970|32.6290|01.0810|00.0010|
|Fire 011819|3000                         |00.0000|00.0000|00.0000|00.0380|00.2190|02.0670|92.6270|05.0490|
|Ethereal 11.38|2976                         |00.0000|00.0000|00.0000|00.0000|00.0000|00.0060|05.0470|94.9470|
