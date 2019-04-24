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

|Engines\Places|1                            |2     |3                                            |4      |5      |6      |7      |8      |
|--------------|-----------------------------|------|---------------------------------------------|-------|-------|-------|-------|-------|
|Stockfish 19040612|99.9770                      |00.0230|00.0000                                      |00.0000|00.0000|00.0000|00.0000|00.0000|
|LCZero v0.21.1-n41800|00.0230                      |99.6630|00.3140                                      |00.0000|00.0000|00.0000|00.0000|00.0000|
|Komodo 2306.00|00.0000                      |00.3140|82.5300                                      |12.8700|03.4740|00.8090|00.0030|00.0000|
|AllieStein v0.3dev-n6.1|00.0000                      |00.0000|08.7850                                      |34.4190|34.3540|22.0740|00.3680|00.0000|
|KomodoMCTS 2306.00|00.0000                      |00.0000|02.7450                                      |22.8040|31.2390|42.3990|00.8120|00.0010|
|Houdini 6.03  |00.0000                      |00.0000|05.6250                                      |29.8830|30.7250|32.6440|01.1210|00.0020|
|Fire 011819   |00.0000                      |00.0000|00.0010                                      |00.0240|00.2080|02.0670|92.6830|05.0170|
|Ethereal 11.38|00.0000                      |00.0000|00.0000                                      |00.0000|00.0000|00.0070|05.0130|94.9800|
