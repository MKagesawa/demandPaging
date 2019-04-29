## Run
python3 demandPaging.py 10 10 20 1 10 lru 0

For the last input value, use 11 to display random values used

### Inputs
The program is invoked with 6 command line arguments, 5 positive integers and one string
- M, the machine size in words.
- P, the page size in words.
- S, the size of each process, i.e., the references are to virtual addresses 0..S-1.
- J, the ‘‘job mix’’, which determines A, B, and C, as described below.
- N, the number of references for each process.
- R, the replacement algorithm, FIFO, RANDOM, or LRU.

### F inputs
- J=1: One process with A=1 and B=C=0, the simplest (fully sequential) case.
- J=2: Four processes, each with A=1 and B=C=0.
- J=3: Four processes, each with A=B=C=0 (fully random references).
- J=4: Four processes. The first process has A=.75, B=.25 and C=0;
The second process has A=.75, B=0, and C=.25;
The third process has A=.75, B=.125 and C=.125;
And the fourth process has A=.5, B=.125 and C=.125.

### example inputs
- 10 10 20 1 10 lru 0
- 10 10 10 1 100 lru 0
- 10 10 10 2 10 lru 0
- 20 10 10 2 10 lru 0
- 20 10 10 2 10 random 0
- 20 10 10 2 10 fifo 0
- 20 10 10 3 10 lru 0
- 20 10 10 3 10 fifo 0
- 20 10 10 4 10 lru 0
- 20 10 10 4 10 random 0