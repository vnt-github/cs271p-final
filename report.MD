- [ ] what's working
    - [ ] under what circumstancces our approach work
    - [ ] why works on some problem instances.

- [ ] what's not working
    - [ ] under what circumstance our approach don't work
    - [ ] why fails on some problem instances.

- [ ] how you did improve you algo based on the observations of results
- [ ] how you'd improve further.
    - [ ] https://1library.net/document/q05xp6gy-enhanced-walksat-finite-learning-automata-max-sat.html
    - [ ] might use 2 or 3 flips instead of 1 flip as it's shown to give better results


- to verify the validity of our max sat solver we created custom test cases as follows
    - satisfiable verification
        - single literal clauses with n total literals and n clauses
            - all true like: 
                - cnf = [(1,), (2,), (3,), (4, ) .... (n, )]
            - true false alternative like:
                - cnf = [(1,), (-2,), (3,), (-4,).....(-(n-1), ) (n,)]
            - our algo is working on it as there is always a free move to be made and it chooses the free move without random or greedy move and it solves .. the n can be as large as 100,000 as it always pick a free move
            - so this can be used to calculate the max_steps value as it's indpendent of noise probability of picking a random move
            - BUT NOTE WE NEED TO KEEP THE MAX_STEPS AS LARGE AS N/2.. else it's difficult
                - for n = 100 we need 50 max_steps
                - for n = 1000 we need 500
    
    - unsatisfiable verification
        - we've tested on the three data set to test the max_set value, and compared the results with rc2 maxSAT solver of pysat(python-sat) library
            - our algo was giving the same number maximum of satisfied.
            - 500 clauses, 10 literas, 3 literals per clause
                - max_flips required: 1. for 10 literals it's quite possible to get good random initial assignment
            - 500 clauses, 30 literas, 3 literals per clause4
                - max_flips required: 40
            - 500 clauses, 50 literas, 3 literals per clause
                - max_flips reqiured: 50
        - here by observation we see that we need no_literals/10 max_flips for correct max_sat value to be found

- by above experimentation we have chooses no_literals/2 to be the max_flips value

- validity of results:
    - early termination
        - cnf: [(1 ,2), (-1, -2), (1 ,-2), (-1 ,2)] this would only result at max 3 satisfied clauses and as it's unsatisfiable it'll always timeout. so early termination should give this result
    - random results of different runs
        - short exhaustive verifications:
            - get the minimized cnf form and verify if all generated results conform to it
                - cnf: [(5 ,-3), (2, 4), (4 ,-5), (1 ,-2), (2, 3)] = TODO: ask if its correct [(1, 4)]
                - cnf: [(3, -1), (-3, 2)] = TODO: ask if its correct [(-1, 2)]
                - the above cnf always generate correct random results on different runs
            - larger generator results verified the assignment with rc2 pysat
                - we have validated the max sat with 2 satisfiable 20_3_100 and 1 unsatisfiable 20_3_100 and 1 unsatisfiable 3_3_100 clauses configuration and we've compared the results with rc2 of pysat2, and it's correct
                - during this we've found that WE NEED TO CHECK THE FIRST INITIAL RANDOM ASSIGNMENT BEFORE FLIPPING, COS IF WE DON'T THEN WE ARE MISSING OUT ON A POTENTIAL BEST ASSIGNMENT.

- random initial assignment more true or more false
    - for satisfiable cnf the initial assignment always converges
    - for unsatisfiable the cnf with either all false or all true often does'nt results in lesser number of satisfied clauses

- optimum value of the noise 
    - 0.1 https://1library.net/document/q05xp6gy-enhanced-walksat-finite-learning-automata-max-sat.html
        - Noise probability: The performance of WSAT depends highly on the walking probability setting which in turns depends on the class of problems to be solved. The plots in Figures 3-4 show 2 selected tests that reflect the general trend observed on almost all the industrial instances tested. Peak performance with respect to the lowest number of unsatisfied clauses is achieved when the walking probability was set to 10.
    - greedy
    - random
    - we've also conducted some experiments and we've found similar results.