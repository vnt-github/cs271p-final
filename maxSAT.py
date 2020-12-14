import sys
import traceback
from time import time
from glob import glob
from random import random, sample

class MAXSatSolver():
    """
    a max sat solver
    """
    def __init__(self, timeout_duration_sec, max_flips, noise):
        self.cnf = []
        self.best_assignment = None
        self.no_vars = None
        self.no_literals_clause = None
        self.no_clauses = None
        self.timeout_duration_sec = timeout_duration_sec
        self.max_flips = max_flips
        self.noise = noise
    
    def _solve(self):
        # everyting is initialized this function logs the final output on success or on interrpt or on timeout
        # handles the timers and other utilities
        try:
            init = time()
            self.best_assignment = None
            self.maxWalkSAT()
        except KeyboardInterrupt:
            print("\nearly terminating the best results are:")

        except Exception:
            traceback.print_exc(file=sys.stdout)
        print("best assignment: {}".format(self.best_assignment))
        print("number of satisfied clauses: {}".format(self.satisfiedCount(self.best_assignment)))
        print("time: %2.6f seconds" % ((time()-init)))
        print('-'*50)

    def solveCNF(self, no_vars, no_literals_clause, no_clauses, cnf):
        self.no_vars = no_vars
        self.no_literals_clause = no_literals_clause
        self.no_clauses = no_clauses
        self.cnf = cnf
        print('no_literals_clause: {} no_clauses: {} no_vars: {}'.format(self.no_literals_clause, self.no_clauses, self.no_vars))
        print('cnf', self.cnf)
        self._solve()


    def solveCNFFiles(self):
        for file_name in glob('tests/max-sat-problem-*.txt'):
            with open(file_name) as file:
                data = file.readlines()
                self.no_vars = int(data[0])
                self.no_literals_clause = int(data[1])
                self.no_clauses = int(data[2])
                self.cnf = []
                for each in data[3:]:
                    self.cnf.append(tuple(map(int, each.split())))
                print('no_literals_clause: {} no_clauses: {} no_vars: {}'.format(self.no_literals_clause, self.no_clauses, self.no_vars))
                print('cnf', self.cnf)
                self._solve()


    def isClauseSatisfied(self, clause, assignment):
        for var in clause:
            if var < 0 and assignment[abs(var)-1] == False or var > 0 and assignment[abs(var)-1] == True:
                return True
        return False

    def breakCount(self, assignment, var):
        before_flip = self.satisfiedCount(assignment)
        self.flip(assignment, var)
        after_flip = self.satisfiedCount(assignment)
        self.flip(assignment, var)
        return max(0, before_flip - after_flip)

    def randomInitialTruthAssignment(self):
        return [random() > 0.5 for _ in range(self.no_vars)]

    def satisfiedCount(self, assignment):
        return sum([1 for clause in self.cnf if self.isClauseSatisfied(clause, assignment)])

    def objective_function(self, assignment):
        return len(self.cnf)-self.satisfiedCount(assignment)

    def getFreeMove(self, clause, assignment):
        for var in clause:
            if self.breakCount(assignment, var) == 0:
                return var
        return None

    def flip(self, assignment, var):
        assignment[abs(var)-1] = not assignment[abs(var)-1]

    def getRandomUnsatisfiedClause(self, assignment):
        return sample([clause for clause in self.cnf if not self.isClauseSatisfied(clause, assignment)], 1)[0]

    def getRandomClauseVar(self, clause):
        return sample(clause, 1)[0]

    def getGreedyClauseVar(self, assignment, clause):
        min_break_count = float('inf')
        best_var = None
        for var in clause:
            break_count = self.breakCount(assignment, var)
            if min_break_count > break_count:
                best_var = abs(var)
                min_break_count = break_count
        return best_var

    def maxWalkSAT(self):
        timeout = time() + self.timeout_duration_sec
        greedy, randoms = 0, 0
        while time() < timeout:
            curr_assignment = self.randomInitialTruthAssignment()
            # print('inital assignment', curr_assignment)
    
            if not self.best_assignment:
                self.best_assignment = curr_assignment
            
            for _ in range(self.max_flips):
                if self.objective_function(curr_assignment) == 0:
                    self.objective_function(curr_assignment)
                    self.best_assignment = curr_assignment
                    print(greedy, randoms)
                    return self.best_assignment
            
                clause = self.getRandomUnsatisfiedClause(curr_assignment)

                var_id = self.getFreeMove(clause, curr_assignment)
                if var_id:
                    self.flip(curr_assignment, var_id)
                    continue
                elif random() < self.noise:
                    randoms += 1
                    var_id = self.getRandomClauseVar(clause)
                else:
                    greedy += 1
                    var_id = self.getGreedyClauseVar(curr_assignment, clause)

                self.flip(curr_assignment, var_id)
                if self.objective_function(curr_assignment) < self.objective_function(self.best_assignment):
                    self.best_assignment = curr_assignment
        print(greedy, randoms)
        return self.best_assignment

if __name__ == "__main__":
    s = MAXSatSolver(120, 1000, 0.25)

    # no_vars = 3
    # cnf = [(3, -1), (-3, 2)]
    # s.solveCNF(no_vars, 2, 2, cnf)
    
    # # NOTE: use below to test the unsatisfied clause and early termination result
    # no_vars = 2
    # cnf = [(1 ,2), (-1, -2), (1 ,-2), (-1 ,2)]
    # s.solveCNF(no_vars, 2, 4, cnf)

    # no_vars = 5
    # cnf = [(5 ,-3), (2, 4), (4 ,-5), (1 ,-2), (2, 3)]
    # s.solveCNF(no_vars, 2, 5, cnf)

    # # NOTE: use below to test the performance
    # no_vars = 1000
    # cnf = [[i, ] if i%2 else [-i,] for i in range(1, no_vars+1)]
    # s.solveCNF(no_vars, 1, no_vars, cnf)

    # no_vars = 1000
    # cnf = [[i, ] for i in range(1, no_vars+1)]
    # s.solveCNF(no_vars, 1, no_vars, cnf)
    s.solveCNFFiles()


