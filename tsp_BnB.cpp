#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <set>
using namespace std;

string dir_path = "./tests_tsp/";
int num_of_cities;
vector<vector<double>> graph;   // using an adjacency matrix to represent the graph of cities

void initGraph(fstream& );
void readInputFile();

void initGraph(fstream& input_file)
{
    string line;

    // read the number of cities
    getline(input_file, line);
    stringstream ss(line);
    ss >> num_of_cities;

    for(int i=0; i<num_of_cities; i++) {
        getline(input_file, line);
        stringstream ss(line);
        vector<double> row(num_of_cities);
        for(int j=0; j<num_of_cities; j++)  // read the path costs from the ith city to jth city
            ss >> row[j];
        graph.push_back(row);
    }
}

void readInputFile()
{
    string input_filename("");
    cout << "Enter the input filename: ";
    cin >> input_filename;
    fstream input_file(dir_path+input_filename);
    if(input_file.is_open()) {
        initGraph(input_file);
        input_file.close();
    } else
        cout << "Unable to open input file: " << input_filename << "\n";
}

void printGraphInfo(vector<vector<double>> graph)
{
    for(int i=0; i<graph.size(); i++) {
        cout << i << "th city: ";
        for(int j=0; j<graph[i].size(); j++) {
            cout << graph[i][j] << "->";
        }
        cout << "null\n";
    }
}

void dfs(vector<vector<double>> graph, set<int>& visited, int cur_vertex, int cost, int& lower_bound)
{
    visited.insert(cur_vertex);
    cout << "cur_vertex: " << cur_vertex << endl;
    if(cost>=lower_bound)
        return;
    if(visited.size()==graph.size()) {
        cost += graph[cur_vertex][0];
        // cout << "graph[cur_vertex][0]: " << graph[cur_vertex][0] << endl;
        cout << "cost: " << cost << endl;
        if(cost<lower_bound) {
            lower_bound = cost;
        } else {
            return;
        }
    }
    for(int i=0; i<graph[cur_vertex].size(); i++) {
        if(visited.find(i)==visited.end()) {
            cost += graph[cur_vertex][i];
            cout << "cost: " << cost << endl;
            dfs(graph, visited, i, cost, lower_bound);
            visited.erase(i);
            cost -= graph[cur_vertex][i];
            cout << "=\n";
        }
    }
}

int branch_and_bound(vector<vector<double>> graph)
{
    set<int> visited;
    int cost = 0, lower_bound = INT_MAX;
    dfs(graph, visited, 0, cost, lower_bound);
    return lower_bound;
}

int main()
{
    // step 0. read input file 
    readInputFile();

    // [test] print graph inforamtion
    cout << "the number of cities: " << num_of_cities << endl;
    cout << "the adjacency matrix of cities: " << endl;
    printGraphInfo(graph);

    // step 1. compute the upper bound

    // step 2. branch and bound algorithm
    int minimum_path_cost = branch_and_bound(graph);
    cout << "minimum_cost: " << minimum_path_cost << "\n";

    return 0;
}