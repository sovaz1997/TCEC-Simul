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

Results after game 161 TCEC 15 Division P:


|Engine                 |Rating |Avg. Scores|1      |2      |3      |4      |5      |6      |7      |8      |
|-----------------------|-------|-----------|-------|-------|-------|-------|-------|-------|-------|-------|
|Stockfish 19040612     |3200   |27.6       |100.0000|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|LCZero v0.21.1-n41800  |3200   |25.5459    |00.0000|100.0000|00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|
|Komodo 2306.00         |3089   |21.43345   |00.0000|00.0000|86.8600|11.0500|02.0900|00.0000|00.0000|00.0000|
|Houdini 6.03           |3100   |20.5251    |00.0000|00.0000|12.1400|23.6600|62.0700|02.1300|00.0000|00.0000|
|AllieStein v0.3dev-n6.1|3079   |20.46555   |00.0000|00.0000|01.0000|64.9000|33.7200|00.3800|00.0000|00.0000|
|KomodoMCTS 2306.00     |3059   |19.5248    |00.0000|00.0000|00.0000|00.3900|02.1200|97.4900|00.0000|00.0000|
|Ethereal 11.38         |2976   |16.93465   |00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|86.8000|13.2000|
|Fire 011819            |3000   |15.97055   |00.0000|00.0000|00.0000|00.0000|00.0000|00.0000|13.2000|86.8000|





