Minesweeper Algorithms

Group Members:
- Armaan Lala alala6@gatech.edu
- Harsha Karanth hkaranth3@gatech
- Kevin Said ksadi3@gatech.edu

Files Submitted
- Algo1.py - This is our algorithm that uses probability to find the best location to look
- Algo2.py - This is our algorithm that uses a reduced minimum constraint idea to find the best spot to dig
- Data folder - This contains all of our captured data that we used for our analysis pdf
- Json Boards Folder - This folder contains all the test cases that we wish to run
- .gitignore - A basic gitignore file used for our version control
- README.txt - A text file containing an overview of the project
- algorithm.pdf - A pdf containing our analysis of Algo1 and Algo2




Desired File Structure: (In case the submission messes with structure)
ArmaanLala-HarshaKaranth-KevinSadi.zip
| --minesweeper-3510/
    | -- Algo1.py
    | -- Algo1.py
    | -- data/
        | -- All stats computed by both algorithms
    | -- json_board/
        | -- All varied test boards to be ran
| -- .gitignore
| -- README.txt
| -- algorithm.pdf




How to Run:
Both algorithms will run ALL .json files that is in the same level directory or in any subfolders in relation to the python files. For this reason, we have one folder labeled 'json_boards/'. If you wish to test the output of any specific json files, please place them in this folder and delete any json files that you do not want to be run. 

We do use external python packages so here are all the import statements we have
import json
import math
import numpy as np
from numpy import unravel_index
import os
import random
import sys
import time
import glob

numpy is probably the only external library that needs to be installed and this can be done either by using `pip3 numpy` or `pip numpy`.

In order to run each one of the algoritms, make sure you are within the minesweeper-3510 folder and run `python3 Algo1.py` or `python3 Algo1.py`. If your system does not support `python3`, then simply type in python.




Bugs/Limitations:

At this moment, using all the test cases provided to us, we do not know of any bugs that occur within our code. 
The only limitation deals with the fact that we must run every single .json file every time instead of being able to test one board at a time.