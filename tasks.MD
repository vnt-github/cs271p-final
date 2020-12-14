- [ ] TODO:
    - [ ] implement and exit and return the current best result option in the code.

- [ ] lecture: 

    - [ ] no particular level of performance is required except TRIVIAL
        - [ ] should show some learning
        - [ ] whats TRIVIAL
            - [ ] gonna get benchmark lower level on monday
    - [ ] no bugs and code run

    - [ ] timeout in range few minutes to an hour.


    - [ ] approach should not be trivial
        - [ ] can you give example of what's TRIVIAL.
    
    - [ ] grading is on
        - [ ] doing testing, experimentation
            - [ ] making sense of stuff
            - [ ] analysis and improving

            - [ ] make observatinos
            - [ ] anything interesting in data
            - [ ] why can't it work.



- [ ] find the optimal value of the p
    - [ ] reserach online
        - [ ] can't find yet
    - [ ] experimentation
- [ ] compare with the greedy approach
- [ ] compare with simulated annealing
    - [ ] did't work


---
# discussions:

what is trivial

what should be done if not satisfiable .. it'll timeout

what should be good value for noise

do we need to do the  clearance of clauses.. ie remove sington and false clause

randomInitialTruthAssignment its random value is 0.5 is it correct

language python vs cpp

printing what should be start node
    follow the input so use the 

will our start will always be the first node

    start from which node

        it should not be specified

need prodigals

    verify the results need to ask

what's trivial

publish some benchmark problems next monday

    smaller scales to simpler levels 


brute force might be able to solve increase the level. publish 10 problems

press the button to stop the ai.

check finished/optimized algo somewehre on the net that you can give the same input -- see if they match

how do we compare

professor will grade the project himself



---
- [ ] i'd improve by setting dynamic max_flips ... rather than having a constant max flips .. i'll have it set to len(cnf)/some_value
    - [ ] need to find some value
    - [ ] if there is some improvement then i'd reset the max flips for the current iteration to try longer for better iteration.

- [ ] test performance against full greedy algo