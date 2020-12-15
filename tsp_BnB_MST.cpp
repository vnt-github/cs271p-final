#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <set>
#include <algorithm>
#include <chrono>
using namespace std;

class Edge {
public:
    int start_vertex;
    int end_vertex;
    double cost;
    // constructors
    Edge(int v, int u, double c): start_vertex(v), end_vertex(u), cost(c) {}; 
};

string dir_path = "./tests_tsp/";
int num_of_cities;
double upper_bound_MST;
vector<vector<double>> graph;   // using an adjacency matrix to represent the graph of cities
vector<int> optimal_route;      // to record the path of the optimal route
vector<Edge> cities_edges;
// vector<int> subset;

void initGraph(fstream& );
void readInputFile();
void printGraphInfo(vector<vector<double>> graph);
void printOptimalRoute();
void printElapsedTime(chrono::steady_clock::time_point start, chrono::steady_clock::time_point end);
void dfs_with_bound(set<int>& visited, int cur_vertex, double cost, double& lower_bound, vector<int> current_route);
double tsp_branch_and_bound();
void dfs_without_bnb(set<int>& visited, int cur_vertex, double cost, double& lower_bound, vector<int> current_route);
double tsp_without_bnb();
double computeMSTWithKruskal(set<int> visited);


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
        for(int j=0; j<num_of_cities; j++) { // read the path costs from the ith city to jth city
            ss >> row[j];
            if(j>=i+1) {    // initialize edge list for Kruskal's algorithm
                Edge edge = Edge(i, j, row[j]);
                cities_edges.push_back(edge);
            }
        }
        graph.push_back(row);
    }
}

void readInputFile()
{
    string input_filename("");
    cout << "Enter the input filename: ";
    cin >> input_filename;
    fstream input_file(dir_path+input_filename+".txt");
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

void printCitiesEdgesInfo()
{
    for(int i=0; i<cities_edges.size(); i++) {
        cout << cities_edges[i].start_vertex << " ";
        cout << cities_edges[i].end_vertex << " ";
        cout << cities_edges[i].cost << "\n";
    }
}

void printOptimalRoute()
{
    for(int i:optimal_route)
        cout << i << " ";
    cout << "\n";
}

void printElapsedTime(chrono::steady_clock::time_point start, chrono::steady_clock::time_point end)
{
    cout << "\tElapsed time in milliseconds: "
        << chrono::duration_cast<chrono::milliseconds>(end - start).count() 
        << " ms\n";
}

void dfs_with_bound(set<int>& visited, int cur_vertex, double cost, double& lower_bound, vector<int> current_route)
{
    visited.insert(cur_vertex);
    if(cost>=lower_bound)
        return;

    if(visited.size()==graph.size()) {
        cost += graph[cur_vertex][0];
        current_route.push_back(cur_vertex);
        if(cost<lower_bound) {
            lower_bound = cost;
            optimal_route = current_route;
        }
        else
            return;
    }

    for(int i=0; i<graph[cur_vertex].size(); i++) {
        if(visited.find(i)==visited.end()) {
            cost += graph[cur_vertex][i];
            current_route.push_back(cur_vertex);
            dfs_with_bound(visited, i, cost, lower_bound, current_route);
            visited.erase(i);
            current_route.pop_back();
            cost -= graph[cur_vertex][i];
        }
    }
}

double tsp_branch_and_bound()
{
    set<int> visited;
    double cost = 0, lower_bound = INT_MAX;
    vector<int> current_route;
    dfs_with_bound(visited, 0, cost, lower_bound, current_route);
    optimal_route.push_back(0);
    return lower_bound;
}

void dfs_without_bnb(set<int>& visited, int cur_vertex, double cost, double& lower_bound, vector<int> current_route)
{
    visited.insert(cur_vertex);

    if(visited.size()==graph.size()) {
        cost += graph[cur_vertex][0];
        current_route.push_back(cur_vertex);
        if(cost<lower_bound) {
            lower_bound = cost;
            optimal_route = current_route;
        }
        else
            return;
    }

    for(int i=0; i<graph[cur_vertex].size(); i++) {
        if(visited.find(i)==visited.end()) {
            cost += graph[cur_vertex][i];
            current_route.push_back(cur_vertex);
            dfs_without_bnb(visited, i, cost, lower_bound, current_route);
            visited.erase(i);
            current_route.pop_back();
            cost -= graph[cur_vertex][i];
        }
    }
}

double tsp_without_bnb()
{
    set<int> visited;
    double cost = 0, lower_bound = INT_MAX;
    vector<int> current_route;
    dfs_without_bnb(visited, 0, cost, lower_bound, current_route);
    optimal_route.push_back(0);
    return lower_bound;
}

void dfs_with_bound_MST(set<int>& visited, int cur_vertex, double cost, double& lower_bound, vector<int> current_route)
{
    double heuristic = computeMSTWithKruskal(visited);
    visited.insert(cur_vertex);
    // strong f(n) = g(n) + h(n)
    double evaluation = cost + heuristic;
    // cout << "cur: " << cur_vertex;
    // cout << "  cost: " << cost;
    // cout << "  heuristic: " << heuristic;
    // cout << "  evaluation: " << evaluation << endl;
    if(evaluation>upper_bound_MST)
        return;
    
    // weak f(n): evaluation function
    // if(cost>upper_bound_MST)
    //     return;

    if(visited.size()==graph.size()) {
        cost += graph[cur_vertex][0];
        current_route.push_back(cur_vertex);
        if(cost<lower_bound) {
            lower_bound = cost;
            optimal_route = current_route;
        }
        else
            return;
    }

    for(int i=0; i<graph[cur_vertex].size(); i++) {
        if(visited.find(i)==visited.end()) {
            cost += graph[cur_vertex][i];
            current_route.push_back(cur_vertex);
            dfs_with_bound_MST(visited, i, cost, lower_bound, current_route);
            visited.erase(i);
            current_route.pop_back();
            cost -= graph[cur_vertex][i];
        }
    }
}

double tsp_branch_and_bound_MST()
{
    set<int> visited;
    double cost = 0, lower_bound = INT_MAX;
    vector<int> current_route;
    dfs_with_bound_MST(visited, 0, cost, lower_bound, current_route);
    optimal_route.push_back(0);
    return lower_bound;
}

void printSubset(vector<int>& subset)
{
    cout << "subset: ";
    for(int i=0; i<num_of_cities; i++)
        cout << subset[i] << " ";
    cout << "\n";
}

void initialize_subset(vector<int>& subset, set<int>& visited)
{
    for(int i=0; i<num_of_cities; i++) {
        if(visited.find(i)!=visited.end())
            subset.push_back(0);
        else
            subset.push_back(i);
    }
}

bool non_decreasing_comp(Edge u, Edge v)
{
    return u.cost < v.cost;
}

int find(vector<int>& subset, int u)
{
    return subset[u];
}

void union_u_v(vector<int>& subset, int u, int v)
{
    for(int i=0; i<subset.size(); i++) {
        if(subset[i]==subset[v])
            subset[i] = subset[u];
    }
}

double computeMSTWithKruskal(set<int> visited)
{
    // sort(cities_edges.begin(), cities_edges.end(), non_decreasing_comp);
    vector<int> subset;
    initialize_subset(subset, visited);
    double res=0;
    for(int i=0; i<cities_edges.size(); i++) {
        // cout << "\t";
        // printSubset(subset);
        if(find(subset, cities_edges[i].start_vertex)!=find(subset, cities_edges[i].end_vertex)) {
            union_u_v(subset, cities_edges[i].start_vertex, cities_edges[i].end_vertex);
            res += cities_edges[i].cost;
        }
    }

    return res;
}

int main()
{
    // step 0. read input file 
    readInputFile();

    // [test] print graph inforamtion
    cout << "the number of cities: " << num_of_cities << endl;
    // cout << "the adjacency matrix of cities: " << endl;
    // printGraphInfo(graph);
    // printCitiesEdgesInfo();

    // step 1-1. sort the edges for Kruskal's algorithm
    sort(cities_edges.begin(), cities_edges.end(), non_decreasing_comp);
    // step 1-2. compute the upper bound using Kruskal's algorithm
    upper_bound_MST = computeMSTWithKruskal({})*2;

    
    // step 2-1. Normal DFS algorithm
    cout << "\tBrute Force Depth-First Search:\n";
    auto start = chrono::steady_clock::now();
    double minimum_path_cost = tsp_without_bnb();
    auto end = chrono::steady_clock::now();
    cout << "\tthe minimum path cost: " << minimum_path_cost << "\n";
    cout << "\tthe path of optimal route: ";
    printOptimalRoute();
    printElapsedTime(start, end);
    
    // step 2-2. branch and bound algorithm
    cout << "\nDepth-First Search Branch and Bound:\n";
    start = chrono::steady_clock::now();
    minimum_path_cost = tsp_branch_and_bound();
    end = chrono::steady_clock::now();
    cout << "\tthe minimum path cost: " << minimum_path_cost << "\n";
    cout << "\tthe path of optimal route: ";
    printOptimalRoute();
    printElapsedTime(start, end);

    // step 2-3. Optimized DFS-BnB algorithm with
    cout << "\nOptimized Depth-First Search Branch and Bound:\n";
    start = chrono::steady_clock::now();
    minimum_path_cost = tsp_branch_and_bound_MST();
    end = chrono::steady_clock::now();
    cout << "\tthe minimum path cost: " << minimum_path_cost << "\n";
    cout << "\tthe path of optimal route: ";
    printOptimalRoute();
    printElapsedTime(start, end);

    return 0;
}