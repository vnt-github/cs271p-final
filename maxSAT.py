import sys
import traceback
import argparse
from time import time
from glob import glob
from random import random, sample, seed
from collections import Counter
class MAXSatSolver():
    """
    a max sat solver object
    """
    def __init__(self, timeout_duration_sec, max_flips=1000, noise=0.1):
        """
        a constructor for max sat solver
        
        Keyword arguments:
        timeout_duration_sec -- the maximum time in seconds our solver will spend on finding the best max sat solution 
        max_flips -- maximum number of flips each iterative try is allowed to perform
        noise -- the probability with which we pick a random move instead of a greedy move
        """
        self.cnf = []
        self.best_assignment = None
        self.no_vars = None
        self.no_literals_clause = None
        self.no_clauses = None
        self.timeout_duration_sec = timeout_duration_sec
        self.max_flips = max_flips
        self.noise = noise
        self.tried_count = Counter()
        seed()
    
    def _solve(self):
        """
        wrapper function to call after the object has been initiated by either solveCNF or solveCNFFiles function
        """
        # everyting is initialized this function logs the final output on success or on interrpt or on timeout
        # handles the timers and other utilities
        try:
            init = time()
            self.best_assignment = None
            # NOTE: by our observation of all true and alternte true, false n clauses cnf we need at least n/2 max_flips for best performance for satisfiable clauses
            self.max_flips = self.no_clauses/2 + 1
            self.tried_count = Counter()
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
        """
        solve a particular cnf

        Keyword arguments:
        cnf -- the Conjuctive Normal Form to be solved for maximum satisfiability
        no_clauses -- number of clauses in the cnf
        no_vars -- number of variables or literals involved in the cnf
        no_literals_clause -- number of literals each clause of cnf have for eg 3-CNF
        """
        self.no_vars = no_vars
        self.no_literals_clause = no_literals_clause
        self.no_clauses = no_clauses
        self.cnf = cnf
        print('no_literals_clause: {} no_clauses: {} no_vars: {}'.format(self.no_literals_clause, self.no_clauses, self.no_vars))
        print('cnf', self.cnf)
        print('|time \t| # clauses_satisfied \t| retry_# \t| flip_#\t|')
        self._solve()


    def solveCNFFiles(self, absolute_path):
        """
        solve all the problem files located at the absolute_path generated in the format defined by generator
        https://github.com/baiqiushi/cs271p/blob/20a562c8b33125a8bdc8f9ce312a2622c328fabd/genMaxSAT.py

        Keyword arguments:
        absolute_path: absolute forward / path of the directory containing max-SAT problem files
        for example: /mnt/c/cs271p-final/tests/benchmarks/
        """
        for file_name in glob(absolute_path + '/*'):
            try:
                with open(file_name) as file:
                    data = file.readlines()
                    self.no_vars = int(data[0])
                    self.no_literals_clause = int(data[1])
                    self.no_clauses = int(data[2])
                    self.cnf = []
                    for each in data[3:]:
                        each = each.strip()
                        if each:
                            self.cnf.append(tuple(map(int, each.split())))
                    print('no_literals_clause: {} no_clauses: {} no_vars: {}'.format(self.no_literals_clause, self.no_clauses, self.no_vars))
                    print('cnf', self.cnf)
                    print('|time \t| # clauses_satisfied \t| retry_# \t| flip_#\t|')
                    self._solve()
            except Exception as err:
                print "Error parsing some file in", absolute_path, "\nerr:", err
                print "-"*50


    def isClauseSatisfied(self, clause, assignment):
        """
        check if the @param clause is satisfied by @param assignment
        """
        for var in clause:
            if (var < 0 and assignment[abs(var)-1] == False) or (var > 0 and assignment[abs(var)-1] == True):
                return True
        return False

    def breakCount(self, assignment, var):
        """
        The Number of currently satisfied Clauses in the self.cnf
        which will become unsatisfied by @param assignment
        if we flipped the value of variable @param var.
        """
        before_flip_assignment = assignment[:]
        self.flip(assignment, var)
        after_flip_assignment = assignment[:]
        self.flip(assignment, var)

        break_count = 0

        for clause in self.cnf:
            if self.isClauseSatisfied(clause, before_flip_assignment) and not self.isClauseSatisfied(clause, after_flip_assignment):
                break_count += 1

        return break_count

    def getCompressedKey(self, assignment):
        """
        get compressed key to check to avoid retried initial assignment with lower probabililty
        """
        key = []
        prev = assignment[0]
        count = 0
        for each in assignment:
            if prev == each:
                count += 1
            else:
                key.append(('1' if not each else '0') + str(count))
                count = 1
                prev = each
        if count:
            key.append(('1' if each else '0') + str(count))

        return '_'.join(key)
        
    def randomInitialTruthAssignment(self):
        """
        get a initial random truth assignment
        """
        # NOTE: experimentational data with all true and all false assignment, aligns with logical inference of setting equal probability of true and false for the best result
        # as the steps to reach the maxima for the initial assignment will be lower in equi distributed true false assignment.
        init = [random() > 0.5 for _ in range(self.no_vars)]
        compressed_key = self.getCompressedKey(init)
        self.tried_count[compressed_key] += 1
        max_attempts = 10
        while max_attempts and 1.0/self.tried_count[compressed_key] < random():
            max_attempts -= 1
            init = [random() > 0.5 for _ in range(self.no_vars)]
            compressed_key = self.getCompressedKey(init)
            self.tried_count[compressed_key] += 1
        return init

    def satisfiedCount(self, assignment):
        """
        return the number of clauses satisfied of self.cnf by @param assignment
        """
        return sum([1 for clause in self.cnf if self.isClauseSatisfied(clause, assignment)])

    def objective_function(self, assignment):
        """
        the objective function guiding our search for an optimum solution with minimum value of objective function
        """
        return len(self.cnf)-self.satisfiedCount(assignment)

    def getFreeMove(self, clause, assignment):
        """
        try and find a variable from @param clause such that its break count is 0
        such a move is free move as it flipping does'nt cost any unwanted side effect. 
        """
        for var in clause:
            if self.breakCount(assignment, var) == 0:
                return var
        return None

    def flip(self, assignment, var):
        """
        invert the value of @param var in the @param assignment
        """
        assignment[abs(var)-1] = not assignment[abs(var)-1]

    def getRandomUnsatisfiedClause(self, assignment):
        """
        return with a uniform random distribution a random unsatisfied clause
        """
        return sample([clause for clause in self.cnf if not self.isClauseSatisfied(clause, assignment)], 1)[0]

    def getRandomClauseVar(self, clause):
        """
        return with uniform random distribution a variable from @param clause
        """
        return sample(clause, 1)[0]

    def getGreedyClauseVar(self, assignment, clause):
        """
        return a var from @param claues such that flipping it reaps the maximum benefit
        ie. return a variable with the minimum break count
        """
        min_break_count = float('inf')
        best_var = None
        for var in clause:
            break_count = self.breakCount(assignment, var)
            if min_break_count > break_count:
                best_var = abs(var)
                min_break_count = break_count
        return best_var

    def maxWalkSAT(self):
        """
        a walkSAT based max SAT solver
        """
        init = time()
        timeout = time() + self.timeout_duration_sec
        retry_i = 1
        while time() < timeout:
            curr_assignment = self.randomInitialTruthAssignment()
            retry_i += 1
    
            if not self.best_assignment:
                self.best_assignment = curr_assignment[:]
            
            for flip_i in range(self.max_flips):
                if self.objective_function(curr_assignment) == 0:
                    self.objective_function(curr_assignment)
                    self.best_assignment = curr_assignment[:]
                    print "%2.6f" % (time()-init), "\t",self.satisfiedCount(curr_assignment), "\t\t\t",retry_i, "\t\t",flip_i
                    return self.best_assignment
            
                clause = self.getRandomUnsatisfiedClause(curr_assignment)

                var_id = self.getFreeMove(clause, curr_assignment)
                if not var_id:
                    if random() < self.noise:
                        var_id = self.getRandomClauseVar(clause)
                    else:
                        var_id = self.getGreedyClauseVar(curr_assignment, clause)

                # NOTE: this is the case to handle if the first random initial assignment has a more clauses satisfied before fliping
                # observer in the 'cnf': [(1, 2, 3), (-2, -1, 3), (1, -3, 2), (1, 2, -3), (1, -2, -3), (2, -3, 1), (-3, 1, -2), (-2, 3, -1), (-3, -1, -2), (-1, -2, 3), (2, -3, 1), (-1, -2, 3), (2, -1, -3), (-3, 1, 2), (2, 3, -1), (1, 3, -2), (3, -2, 1), (2, 3, 1), (-1, -3, -2), (-2, 3, 1), (-2, 1, 3), (1, 2, 3), (-3, 2, 1), (-3, -2, 1), (-1, 3, -2), (2, 3, -1), (-2, -3, 1), (-2, -1, 3), (-2, 1, 3), (-2, -3, -1), (2, -3, 1), (-1, -3, 2), (-1, 2, 3), (-3, -1, 2), (-2, 1, -3), (-1, -2, 3), (-2, -3, -1), (3, -1, 2), (-2, 3, 1), (-2, 1, -3), (2, -3, -1), (3, -2, -1), (-1, -3, -2), (-1, 2, 3), (-2, 1, 3), (1, -3, -2), (2, 1, -3), (-3, -1, 2), (-3, -2, 1), (-3, -1, -2), (2, 1, -3), (1, 3, 2), (1, -2, 3), (-3, 2, -1), (1, -2, 3), (-1, 2, -3), (-2, -1, 3), (-3, 1, -2), (-2, 3, 1), (-1, -2, -3), (2, 3, 1), (-2, 1, -3), (-2, -1, -3), (2, 1, -3), (-2, -1, 3), (1, 2, -3), (-1, -2, 3), (-3, -2, -1), (-2, -1, -3), (2, 3, 1), (1, -3, -2), (-1, 2, 3), (-1, -3, 2), (-1, -3, 2), (3, 1, 2), (-2, -1, 3), (3, -1, -2), (-1, -3, -2), (-1, 3, -2), (2, -3, -1), (1, 3, 2), (3, -1, -2), (2, 3, 1), (2, 1, -3), (2, -1, 3), (3, 2, 1), (-1, -3, 2), (-3, 2, 1), (-1, -3, -2), (-2, 3, -1), (2, -1, -3), (3, -1, 2), (-3, 2, 1), (3, -2, -1), (-1, -3, -2), (2, -1, -3), (-3, 2, -1), (-3, 2, 1), (-1, 3, 2), (-3, -2, 1)]
                # with [True, False, False] giving 91 satisfied clauses where [False, False, False] gives 90 satisfied clauses
                if flip_i == 0 and self.objective_function(curr_assignment) < self.objective_function(self.best_assignment):
                    print "%2.6f" % (time()-init), "\t",self.satisfiedCount(curr_assignment), "\t\t\t",retry_i, "\t\t",flip_i

                    # print('retry_i: {} flip_i: {} prev_clauses_satisfied: {} new_clauses_satisfied: {}'.format(retry_i, flip_i, self.satisfiedCount(self.best_assignment), self.satisfiedCount(curr_assignment)))
                    self.best_assignment = curr_assignment[:]

                self.flip(curr_assignment, var_id)
                if self.objective_function(curr_assignment) < self.objective_function(self.best_assignment):
                    print "%2.6f" % (time()-init), "\t",self.satisfiedCount(curr_assignment), "\t\t\t",retry_i, "\t\t",flip_i
                    # print('retry_i: {} flip_i: {} prev_clauses_satisfied: {} new_clauses_satisfied: {}'.format(retry_i, flip_i, self.satisfiedCount(self.best_assignment), self.satisfiedCount(curr_assignment)))
                    self.best_assignment = curr_assignment[:]

        return self.best_assignment


def main():
    parser = argparse.ArgumentParser(description="Solve all MAX-SAT problem in the directory given by path as argument")
    
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument("-d", "--absolute_path", help="absolute path of the directory containing MAX-SAT problem files as defined in the generator", required=True)
    
    optional.add_argument("-t", "--timeout_in_seconds", help="maximum run time in seconds for each problem file", required=False, default=10)
    optional.add_argument('-p', "--noise", help="noise probability of random move", required=False, type=float, default=0.1)
    optional.add_argument('-m', "--max_flips", help="max flips allowed for each try", required=False, type=int, default=1000)

    args = parser.parse_args()
    s = MAXSatSolver(args.timeout_in_seconds, args.max_flips, args.noise)
    s.solveCNFFiles(args.absolute_path)

if __name__ == "__main__":
    main()
    # s = MAXSatSolver(10)

    # print(s.getCompressedKey([True, False, True, False]))
    # print(s.getCompressedKey([True, True, True, True]))
    # print(s.getCompressedKey([True, True, False, False, True]))
    # print(s.getCompressedKey([True, False, False, False, True, False]))
    # for max_steps in range(10, 150, 10):
    #     print('max_steps: {}'.format(max_steps))
    #     s = MAXSatSolver(30, max_steps, 0.2)
    #     s.solveCNFFiles()
   
    # no_vars = 100
    # for max_steps in range(10, no_vars, 10):
    #     print 'max_steps:', max_steps
    #     s = MAXSatSolver(10, max_steps, 0.2)
    #     # cnf = [[i, ] for i in range(1, no_vars+1)]
    #     cnf = [[i, ] if i%2 else [-i,] for i in range(1, no_vars+1)]
    #     s.solveCNF(no_vars, 1, no_vars, cnf)
    
    # s = MAXSatSolver(180)
    # for _ in range(10):
    #     no_vars = 3
    #     cnf = [(3, -1), (-3, 2)]
    #     s.solveCNF(no_vars, 2, 2, cnf)

    #     no_vars = 5
    #     cnf = [(5 ,-3), (2, 4), (4 ,-5), (1 ,-2), (2, 3)]
    #     s.solveCNF(no_vars, 2, 5, cnf)
    # s.solveCNFFiles('/mnt/c/cs271p-final/tests/benchmarks')

    # # NOTE: use below to test the unsatisfied clause and early termination result
    # no_vars = 2
    # cnf = [(1 ,2), (-1, -2), (1 ,-2), (-1 ,2)]
    # s.solveCNF(no_vars, 2, 4, cnf)
    # for noise in range(1, 16, 1):
    #     n = noise/100.0
    #     print('noise:', n)
    #     s = MAXSatSolver(60, 1000, n)
    #     s.solveCNFFiles()

