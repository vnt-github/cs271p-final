# Dependencies
    - python 2.7+
    - pip install argparse (if not already installed)

## (1) maxSAT.py
Max-SAT solver (See details in `maxSAT.py`)
#### usage
```bash
python maxSAT.py -h
python maxSAT.py -d "/mnt/c/cs271p-final/tests/benchmarks"
```
NOTE: make sure -d points to the  folder/directory containing the problem for CNF in the format defined here as below only.
https://github.com/baiqiushi/cs271p/blob/20a562c8b33125a8bdc8f9ce312a2622c328fabd/genMaxSAT.py

Any other files in the directory will not be parsed an will be skipped without terminating the program



this program supports early termination either by USERS INTERRUPT i.e. ^C or if the time runs out

checkout examples in **ExampleRun.png** file in the zip for more info