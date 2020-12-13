#include <iostream>
#include <vector>
#include <chrono>

typedef std::chrono::high_resolution_clock::time_point TimeVar;
#define duration(a) std::chrono::duration_cast<std::chrono::nanoseconds>(a).count()
#define timeNow() std::chrono::high_resolution_clock::now()

using namespace std;

vector<bool> randomInitialTruthAssignment(int no_vars) {
    vector<bool> res;
    for (int i = 0; i < no_vars; i++)
        res.push_back(rand() > 0.5);
    
}

void maxWalkSAT(int no_vars, vector<vector<int>> cnf, int timeout_duration_sec, int max_flips, int noise) {
    TimeVar timeInit=timeNow();
    vector<bool> best_assignment;
    while (duration(timeNow - timeInit) < timeout_duration_sec * 1000000) {
        vector<bool> curr_assignment = randomInitialTruthAssignment(no_vars);

        if (best_assignment.empty())
            best_assignment = curr_assignment;
        
        for (int flip = 0; flip < max_flips; flip++)
        {
            // TODO: complete and compare performance once done with othe priority tasks
        }
    }
}

int main() {
    int no_vars = 100;
    vector<vector<int>> cnf;

    srand(static_cast<unsigned int>(time(nullptr)));
    for (int i = 1; i < no_vars; i++)
        cnf.push_back({i});
    

}