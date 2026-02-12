
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

struct Process {
    int id, arrival, burst, priority;
};

void fcfs(vector<Process> p) {
    int time = 0;
    cout << "\n--- FCFS ---\n";
    for (auto &proc : p) {
        if (time < proc.arrival) time = proc.arrival;
        cout << "P" << proc.id << ": " << time;
        time += proc.burst;
        cout << " -> " << time << endl;
    }
}

void sjf(vector<Process> p) {
    cout << "\n--- SJF (Non-Preemptive) ---\n";
    sort(p.begin(), p.end(), [](Process a, Process b){
        return a.burst < b.burst;
    });
    int time = 0;
    for (auto &proc : p) {
        cout << "P" << proc.id << ": " << time;
        time += proc.burst;
        cout << " -> " << time << endl;
    }
}

void priorityScheduling(vector<Process> p) {
    cout << "\n--- Priority Scheduling ---\n";
    sort(p.begin(), p.end(), [](Process a, Process b){
        return a.priority < b.priority;
    });
    int time = 0;
    for (auto &proc : p) {
        cout << "P" << proc.id << ": " << time;
        time += proc.burst;
        cout << " -> " << time << endl;
    }
}

void roundRobin(vector<Process> p, int quantum) {
    cout << "\n--- Round Robin ---\n";
    queue<Process> q;
    for (auto &proc : p) q.push(proc);
    int time = 0;
    while (!q.empty()) {
        Process proc = q.front(); q.pop();
        int exec = min(quantum, proc.burst);
        cout << "P" << proc.id << ": " << time;
        time += exec;
        cout << " -> " << time << endl;
        proc.burst -= exec;
        if (proc.burst > 0) q.push(proc);
    }
}

int main() {
    int n;
    cin >> n;
    vector<Process> p(n);
    for(int i=0;i<n;i++){
        p[i].id=i+1;
        cin >> p[i].arrival >> p[i].burst >> p[i].priority;
    }
    fcfs(p);
    sjf(p);
    priorityScheduling(p);
    roundRobin(p, 2);
    return 0;
}
