import sys
import traceback
from time import time
from glob import glob
from random import random, sample

best_assignment = None
cnf = []

def isClauseSatisfied(clause, assignment):
    for var in clause:
        if var < 0 and assignment[abs(var)] == False or var > 0 and assignment[abs(var)] == True:
            return True
    return False

def breakCount(cnf, assignment, var):
    before_flip = satisfied_count(cnf, assignment)
    flip(assignment, var)
    return max(0, before_flip - satisfied_count(cnf, assignment))

def randomInitialTruthAssignment(no_vars):
    return [random() > 0.5 for _ in range(no_vars+1)]

def satisfied_count(cnf, assignment):
    return sum([1 for clause in cnf if isClauseSatisfied(clause, assignment)])

def objective_function(cnf, assignment):
    return len(cnf)-satisfied_count(cnf, assignment)

def getFreeMove(clause, cnf, assignment):
    for var in clause:
        if breakCount(cnf, assignment, var) == 0:
            return var
    return None

def flip(assignment, var):
    assignment[abs(var)] = not assignment[abs(var)]

def getRandomUnsatisfiedClause(cnf, assignment):
    return sample([clause for clause in cnf if not isClauseSatisfied(clause, assignment)], 1)[0]

def getRandomClauseVar(clause):
    return sample(clause, 1)[0]

def getGreedyClauseVar(cnf, assignment, clause):
    min_break_count = float('inf')
    best_var = None
    for var in clause:
        break_count = breakCount(cnf, assignment, var)
        if min_break_count > break_count:
            best_var = abs(var)
            min_break_count = break_count
    return best_var

def maxWalkSAT(no_vars, cnf, timeout_duration_sec, max_flips, noise=0.5):
    global best_assignment

    timeout = time() + timeout_duration_sec
    while time() < timeout:
        curr_assignment = randomInitialTruthAssignment(no_vars)
        
        if not best_assignment:
            best_assignment = curr_assignment
        
        for _ in range(max_flips):
            if objective_function(cnf, curr_assignment) == 0:
                best_assignment = curr_assignment
                return best_assignment[1:]
        
            clause = getRandomUnsatisfiedClause(cnf, curr_assignment)

            var_id = getFreeMove(clause, cnf, curr_assignment)
            if var_id:
                flip(curr_assignment, var_id)
                continue
            elif random() < noise:
                var_id = getRandomClauseVar(clause)
            else:
                var_id = getGreedyClauseVar(cnf, curr_assignment, clause)

            flip(curr_assignment, var_id)
            if objective_function(cnf, curr_assignment) < objective_function(cnf, best_assignment):
                best_assignment = curr_assignment

    return best_assignment[1:]


def solveCNFFiles():
    global cnf
    for file_name in glob('tests/max-sat-problem-*.txt'):
        with open(file_name) as file:
            data = file.readlines()
            no_vars, no_literal_clause, no_clause = int(data[0]), int(data[1]), int(data[2])
            for each in data[3:]:
                cnf.append(tuple(map(int, each.split())))
            print('no_literals_clause: {} no_clauses: {} no_vars: {}'.format(no_literal_clause, no_clause, no_vars))
            print('cnf', cnf)
            print(maxWalkSAT(no_vars, cnf, 120, 1000))
def main():
    try:
        init = time()
        solveCNFFiles()
        # no_vars = 20
        # cnf = [(i, ) for i in range(1, no_vars + 1)]
        # print(maxWalkSAT(no_vars, cnf, 120, 100, 1))
        # print(maxWalkSAT(no_vars, cnf, 120, 100, 0.75))
        # print(maxWalkSAT(no_vars, cnf, 120, 100, 0.5))
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"

    except Exception:
        traceback.print_exc(file=sys.stdout)
    print(best_assignment[1:])
    print(satisfied_count(cnf, best_assignment), time()-init)
    print('-'*50)
    sys.exit(0)

if __name__ == "__main__":
    # no_vars = 3
    # cnf = [(3, -1), (-3, 2)]
    # print(maxWalkSAT(no_vars, cnf, 120, 1000))

    # NOTE: use below to test the performance
    # no_vars = 14
    # cnf = [(i, ) for i in range(1, no_vars + 1)]
    # print(maxWalkSAT(no_vars, cnf, 120, 100, 0.5))
    # print(maxWalkSAT(no_vars, cnf, 120, 100, 0.75))
    # print(maxWalkSAT(no_vars, cnf, 120, 100, 1))

    # no_vars = 2
    # cnf = [(1 ,2), (-1, -2), (1 ,-2), (-1 ,2)]
    # print(maxWalkSAT(no_vars, cnf, 120, 1000))

    # no_vars = 5
    # cnf = [(5 ,-3), (2, 4), (4 ,-5), (1 ,-2), (2, 3)]
    # print(maxWalkSAT(no_vars, cnf, 120, 1000))

    # solveCNFFiles()
    # cnf = [(-8, 2, -3), (1, 6, -19), (9, -15, 11), (4, -5, 16), (14, -17, -10), (-13, -7, 18), (-15, -8, -5), (13, 1, 2), (-20, 17, 12), (-10, -7, -14), (-9, 3, 18), (6, -19, -11), (12, -9, -7), (-11, 20, -10), (-2, -8, 5), (-18, 19, 3), (16, -1, 14), (-4, -15, -17), (-6, -20, 3), (-19, -15, 11), (-4, -18, 8), (-1, 9, 2), (-17, 14, 12), (-5, 13, 7), (14, 8, -6), (-13, -17, -15), (-11, -1, -5), (-9, 12, 18), (7, -16, 20), (19, 4, -3), (-11, 10, -8), (3, -9, -5), (-7, 13, 6), (17, -19, -4), (15, 14, -18), (-12, -1, 20), (10, -3, -16), (17, 12, 4), (7, 20, 1), (-18, 6, 14), (-5, 19, 8), (-9, -13, 15), (20, 18, 10), (5, -6, 15), (19, 1, -17), (4, -3, -13), (7, -11, -12), (8, 14, 16), (-7, 19, 3), (18, 2, -4), (8, 9, 10), (16, 5, -17), (1, 6, -20), (15, 11, 12), (18, 17, 13), (-3, 12, -2), (16, -10, 1), (15, 8, -9), (-20, -19, -5), (-6, 14, 7), (12, -4, -17), (8, -2, -9), (5, -11, -1), (16, -6, -20), (18, 7, -15), (14, -3, -13), (-8, 12, -3), (14, -19, -6), (-16, -5, 7), (-13, 10, -1), (17, 18, 11), (-4, -9, -2), (19, 3, 1), (-6, 2, -11), (5, -10, 8), (4, 7, -16), (20, 12, 13), (-18, -15, 17), (-11, 6, -16), (-15, -9, -13), (19, 4, -10), (-2, 12, 5), (18, 3, -8), (14, 17, 20), (17, 19, -16), (-1, 2, 10), (6, -14, 11), (-9, -4, -13), (15, -20, -7), (18, -5, 3), (1, -8, -9), (7, 2, 3), (-19, -6, 11), (-18, -4, -10), (-17, -20, -16), (5, -13, 12), (12, 14, -19), (-16, 1, -5), (7, 8, 18), (6, 15, 9)]
    # assignment = [False, False, True, False, False, False, False, False, False, False, True, False, True, False, True, True, True, True, True, True, True]
    # clause = (4, 7, -16)
    # getGreedyClauseVar(cnf, assignment, clause)
    main()


