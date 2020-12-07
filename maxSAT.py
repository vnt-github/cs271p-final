from time import time
from glob import glob
from random import random, sample
# from future import print

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
        if min_break_count > breakCount:
            best_var = abs(var)
            min_break_count = break_count
    return best_var

def maxWalkSAT(no_vars, cnf, timeout_duration_sec, max_flips, noise=0.5):
    timeout = time() + timeout_duration_sec
    best_assignment = None
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
    for file_name in glob('tests/max-sat-problem-*.txt'):
        with open(file_name) as file:
            data = file.readlines()
            no_vars, no_literal_clause, no_clause = int(data[0]), int(data[1]), int(data[2])
            cnf = []
            for each in data[3:]:
                cnf.append(tuple(map(int, each.split())))
            print('no_literals_clause: {} no_clauses: {} no_vars: {}'.format(no_literal_clause, no_clause, no_vars))
            print('cnf', cnf)
            print(maxWalkSAT(no_vars, cnf, 120, 1000))
            print('-'*50)

if __name__ == "__main__":
    # no_vars = 3
    # cnf = [(3, -1), (-3, 2)]
    # print(maxWalkSAT(no_vars, cnf, 120, 1000))

    # no_vars = 6
    # cnf = [(i, ) for i in range(1, 7)]
    # print(maxWalkSAT(no_vars, cnf, 120, 1000))

    # no_vars = 5
    # cnf = [(5 ,-3), (2, 4), (4 ,-5), (1 ,-2), (2, 3)]
    # print(maxWalkSAT(no_vars, cnf, 120, 1000))

    solveCNFFiles()