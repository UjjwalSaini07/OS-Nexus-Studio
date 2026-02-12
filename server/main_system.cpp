/**
 * Advanced OS - Main System
 * Features: Custom Memory Allocator, Enhanced CPU Scheduler, File Server
 * With Terminal UI and Real-time Status
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iomanip>
#include <sstream>
#include <windows.h>

#pragma comment(lib, "ws2_32.lib")

using namespace std;

// Colors for terminal output
#define RESET   ""
#define RED     ""
#define GREEN   ""
#define YELLOW  ""
#define BLUE    ""
#define CYAN    ""
#define BOLD    ""

#define PORT 9090

// ============== CUSTOM MEMORY ALLOCATOR ==============

class CustomAllocator {
private:
    static const size_t HEAP_SIZE = 1024 * 1024; // 1MB heap
    
    struct Block {
        bool allocated;
        size_t size;
        Block* next;
    };
    
    uint8_t* heap;
    Block* free_list;
    size_t total_allocated;
    size_t total_free;
    
public:
    CustomAllocator() {
        heap = (uint8_t*)VirtualAlloc(NULL, HEAP_SIZE, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (!heap) {
            cerr << "Failed to allocate heap" << endl;
            exit(1);
        }
        free_list = (Block*)heap;
        free_list->allocated = false;
        free_list->size = HEAP_SIZE;
        free_list->next = NULL;
        total_allocated = 0;
        total_free = HEAP_SIZE;
    }
    
    ~CustomAllocator() {
        if (heap) VirtualFree(heap, 0, MEM_RELEASE);
    }
    
    void* allocate(size_t size) {
        // Align to 8 bytes
        size = ((size + 7) / 8) * 8;
        size += sizeof(Block); // Space for block header
        
        Block* prev = NULL;
        Block* current = free_list;
        
        while (current) {
            if (!current->allocated && current->size >= size) {
                // Found suitable block
                if (current->size > size + sizeof(Block) + 16) {
                    // Split block
                    Block* new_block = (Block*)((uint8_t*)current + size);
                    new_block->allocated = false;
                    new_block->size = current->size - size;
                    new_block->next = current->next;
                    
                    current->allocated = true;
                    current->size = size;
                    current->next = new_block;
                    
                    if (prev) prev->next = new_block;
                    else free_list = new_block;
                } else {
                    // Use whole block
                    current->allocated = true;
                    if (prev) prev->next = current->next;
                    else free_list = current->next;
                }
                
                total_allocated += size;
                total_free -= size;
                return (void*)((uint8_t*)current + sizeof(Block));
            }
            prev = current;
            current = current->next;
        }
        
        return NULL; // No suitable block found
    }
    
    void deallocate(void* ptr) {
        if (!ptr) return;
        
        Block* block = (Block*)((uint8_t*)ptr - sizeof(Block));
        block->allocated = false;
        
        total_allocated -= block->size;
        total_free += block->size;
        
        // Merge with next block if free
        Block* current = (Block*)heap;
        while (current) {
            if (!current->allocated && current->next && !current->next->allocated) {
                current->size += current->next->size;
                current->next = current->next->next;
            }
            current = current->next;
        }
    }
    
    void printStats() {
        cout << BOLD << CYAN << "\n=== Memory Allocator Stats ===" << RESET << endl;
        cout << "Total Heap Size: " << HEAP_SIZE / 1024 << " KB" << endl;
        cout << "Allocated: " << total_allocated / 1024 << " KB" << endl;
        cout << "Free: " << total_free / 1024 << " KB" << endl;
        double frag = (total_free > 0) ? (1.0 - (total_free / (double)HEAP_SIZE)) * 100 : 0;
        cout << "Fragmentation: " << fixed << setprecision(2) << frag << "%" << endl;
    }
};

// ============== PROCESS SCHEDULER ==============

struct Process {
    int id;
    int arrival;
    int burst;
    int priority;
    int completion;
    int turnaround;
    int waiting;
    int response;
    bool started;
    
    Process(int i, int a, int b, int p) : id(i), arrival(a), burst(b), 
        priority(p), completion(0), turnaround(0), waiting(0), 
        response(-1), started(false) {}
};

struct GanttEntry {
    int pid;
    int start;
    int end;
};

class EnhancedScheduler {
private:
    vector<Process> processes;
    vector<GanttEntry> gantt;
    bool running;
    int current_time;
    
public:
    EnhancedScheduler() : running(false), current_time(0) {}
    
    void addProcess(int id, int arrival, int burst, int priority) {
        processes.emplace_back(id, arrival, burst, priority);
    }
    
    vector<Process> getProcesses() {
        return processes;
    }
    
    void clear() {
        processes.clear();
        gantt.clear();
        current_time = 0;
    }
    
    void runFCFS() {
        cout << BOLD << GREEN << "\n--- Running FCFS Scheduler ---" << RESET << endl;
        vector<Process> sorted = processes;
        sort(sorted.begin(), sorted.end(), [](const Process& a, const Process& b) {
            return a.arrival < b.arrival;
        });
        
        int time = 0;
        for (size_t i = 0; i < sorted.size(); i++) {
            if (time < sorted[i].arrival) time = sorted[i].arrival;
            gantt.push_back({sorted[i].id, time, time + sorted[i].burst});
            time += sorted[i].burst;
            sorted[i].completion = time;
            sorted[i].turnaround = sorted[i].completion - sorted[i].arrival;
            sorted[i].waiting = sorted[i].turnaround - sorted[i].burst;
            cout << "P" << sorted[i].id << ": " << sorted[i].arrival << " -> " << sorted[i].completion 
                 << " | Waiting: " << sorted[i].waiting << endl;
        }
        printStats(sorted);
    }
    
    void runSJF() {
        cout << BOLD << GREEN << "\n--- Running SJF Scheduler ---" << RESET << endl;
        vector<Process> sorted = processes;
        sort(sorted.begin(), sorted.end(), [](const Process& a, const Process& b) {
            if (a.arrival == b.arrival) return a.burst < b.burst;
            return a.arrival < b.arrival;
        });
        
        int time = 0;
        size_t i = 0;
        priority_queue<pair<int, size_t>, vector<pair<int, size_t>>, greater<pair<int, size_t>>> pq;
        
        while (i < sorted.size() || !pq.empty()) {
            while (i < sorted.size() && sorted[i].arrival <= time) {
                pq.push(make_pair(sorted[i].burst, i));
                i++;
            }
            if (!pq.empty()) {
                pair<int, size_t> top = pq.top();
                pq.pop();
                int burst = top.first;
                size_t idx = top.second;
                gantt.push_back({sorted[idx].id, time, time + burst});
                time += burst;
                sorted[idx].completion = time;
                sorted[idx].turnaround = sorted[idx].completion - sorted[idx].arrival;
                sorted[idx].waiting = sorted[idx].turnaround - sorted[idx].burst;
                cout << "P" << sorted[idx].id << ": " << time - burst << " -> " << time << endl;
            } else {
                time = sorted[i].arrival;
            }
        }
        printStats(sorted);
    }
    
    void runPriority() {
        cout << BOLD << GREEN << "\n--- Running Priority Scheduler ---" << RESET << endl;
        vector<Process> sorted = processes;
        sort(sorted.begin(), sorted.end(), [](const Process& a, const Process& b) {
            if (a.arrival == b.arrival) return a.priority < b.priority;
            return a.arrival < b.arrival;
        });
        
        int time = 0;
        size_t i = 0;
        priority_queue<pair<int, size_t>, vector<pair<int, size_t>>, greater<pair<int, size_t>>> pq;
        
        while (i < sorted.size() || !pq.empty()) {
            while (i < sorted.size() && sorted[i].arrival <= time) {
                pq.push(make_pair(sorted[i].priority, i));
                i++;
            }
            if (!pq.empty()) {
                pair<int, size_t> top = pq.top();
                pq.pop();
                int pri = top.first;
                size_t idx = top.second;
                gantt.push_back({sorted[idx].id, time, time + sorted[idx].burst});
                time += sorted[idx].burst;
                sorted[idx].completion = time;
                sorted[idx].turnaround = sorted[idx].completion - sorted[idx].arrival;
                sorted[idx].waiting = sorted[idx].turnaround - sorted[idx].burst;
                cout << "P" << sorted[idx].id << " (Pri:" << pri << "): " 
                     << time - sorted[idx].burst << " -> " << time << endl;
            } else {
                time = sorted[i].arrival;
            }
        }
        printStats(sorted);
    }
    
    void runRoundRobin(int quantum) {
        cout << BOLD << GREEN << "\n--- Running Round Robin (Quantum=" << quantum << ") ---" << RESET << endl;
        queue<size_t> q;
        vector<bool> in_queue;
        in_queue.assign(processes.size(), false);
        int time = 0;
        size_t i = 0;
        
        for (size_t j = 0; j < processes.size(); j++) {
            if (processes[j].arrival == time) {
                q.push(j);
                in_queue[j] = true;
            }
        }
        
        while (i < processes.size() || !q.empty()) {
            if (!q.empty()) {
                size_t idx = q.front();
                q.pop();
                in_queue[idx] = false;
                
                int exec = min(quantum, processes[idx].burst);
                gantt.push_back({processes[idx].id, time, time + exec});
                cout << "P" << processes[idx].id << ": " << time << " -> " << time + exec << endl;
                
                time += exec;
                processes[idx].burst -= exec;
                
                while (i < processes.size() && processes[i].arrival <= time) {
                    if (!in_queue[i]) {
                        q.push(i);
                        in_queue[i] = true;
                    }
                    i++;
                }
                
                if (processes[idx].burst > 0) {
                    q.push(idx);
                    in_queue[idx] = true;
                } else {
                    processes[idx].completion = time;
                    processes[idx].turnaround = processes[idx].completion - processes[idx].arrival;
                    processes[idx].waiting = processes[idx].turnaround - (exec - (processes[idx].burst + exec));
                }
            } else {
                time = processes[i].arrival;
            }
        }
        printStats(processes);
    }
    
    void printStats(const vector<Process>& procs) {
        double total_wt = 0, total_tat = 0;
        cout << BOLD << CYAN << "\n--- Scheduling Statistics ---" << RESET << endl;
        cout << "ID\tAT\tBT\tCT\tTAT\tWT" << endl;
        cout << "----------------------------------------" << endl;
        for (size_t k = 0; k < procs.size(); k++) {
            const Process& p = procs[k];
            cout << "P" << p.id << "\t" << p.arrival << "\t" << p.burst << "\t" 
                 << p.completion << "\t" << p.turnaround << "\t" << p.waiting << endl;
            total_wt += p.waiting;
            total_tat += p.turnaround;
        }
        cout << "----------------------------------------" << endl;
        cout << "Avg Waiting Time: " << fixed << setprecision(2) << total_wt / procs.size() << endl;
        cout << "Avg Turnaround Time: " << fixed << setprecision(2) << total_tat / procs.size() << endl;
    }
    
    void printGantt() {
        cout << BOLD << YELLOW << "\n--- Gantt Chart ---" << RESET << endl;
        cout << "|";
        for (size_t i = 0; i < gantt.size(); i++) {
            cout << " P" << gantt[i].pid << " |";
        }
        cout << endl;
        cout << "0";
        int time = 0;
        for (size_t i = 0; i < gantt.size(); i++) {
            time = gantt[i].end;
            cout << "    " << time;
        }
        cout << endl;
    }
    
    vector<GanttEntry> getGantt() { return gantt; }
};

// ============== ENHANCED FILE SERVER ==============

class EnhancedFileServer {
private:
    SOCKET server_fd;
    sockaddr_in address;
    bool running;
    int client_count;
    
public:
    EnhancedFileServer() : server_fd(INVALID_SOCKET), running(false), client_count(0) {
        WSADATA wsaData;
        WSAStartup(MAKEWORD(2, 2), &wsaData);
    }
    
    ~EnhancedFileServer() {
        stop();
        WSACleanup();
    }
    
    bool start() {
        server_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (server_fd == INVALID_SOCKET) return false;
        
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(PORT);
        
        if (bind(server_fd, (sockaddr*)&address, sizeof(address)) == SOCKET_ERROR) {
            closesocket(server_fd);
            return false;
        }
        
        if (listen(server_fd, 10) == SOCKET_ERROR) {
            closesocket(server_fd);
            return false;
        }
        
        running = true;
        cout << BOLD << GREEN << "[SERVER] File server started on port " << PORT << RESET << endl;
        return true;
    }
    
    void stop() {
        running = false;
        if (server_fd != INVALID_SOCKET) {
            closesocket(server_fd);
        }
        cout << BOLD << RED << "[SERVER] File server stopped" << RESET << endl;
    }
    
    void handleClient(SOCKET sock) {
        client_count++;
        cout << BOLD << BLUE << "[SERVER] Client " << client_count << " connected" << RESET << endl;
        
        char buffer[1024] = {0};
        recv(sock, buffer, 1024, 0);
        
        string command(buffer);
        string response;
        
        if (command == "LIST") {
            response = "Available files:\n";
            WIN32_FIND_DATAA findFileData;
            HANDLE hFind = FindFirstFileA("*", &findFileData);
            if (hFind != INVALID_HANDLE_VALUE) {
                do {
                    if (!(findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
                        response += "  - " + string(findFileData.cFileName) + "\n";
                    }
                } while (FindNextFileA(hFind, &findFileData));
                FindClose(hFind);
            }
        } else if (command.substr(0, 4) == "GET ") {
            string filename = command.substr(4);
            ifstream file(filename);
            if (!file.is_open()) {
                response = "ERROR: File not found";
            } else {
                string line;
                while (getline(file, line)) {
                    response += line + "\n";
                }
                file.close();
            }
        } else if (command.substr(0, 4) == "INFO ") {
            string filename = command.substr(4);
            ifstream file(filename, ios::binary | ios::ate);
            if (file.is_open()) {
                streamsize size = file.tellg();
                response = "OK: " + to_string(size) + " bytes";
            } else {
                response = "ERROR: File not found";
            }
        } else {
            response = "ERROR: Unknown command. Use LIST, GET <filename>, or INFO <filename>";
        }
        
        send(sock, response.c_str(), response.size(), 0);
        closesocket(sock);
        cout << BLUE << "[SERVER] Client " << client_count << " disconnected" << RESET << endl;
    }
    
    void run() {
        cout << BOLD << CYAN << "[SERVER] Waiting for connections..." << RESET << endl;
        while (running) {
            SOCKET new_socket = accept(server_fd, NULL, NULL);
            if (new_socket != INVALID_SOCKET) {
                handleClient(new_socket);
            }
        }
    }
};

// ============== MAIN MENU ==============

void printBanner() {
    cout << BOLD << YELLOW << R"(
    =======================================
        ADVANCED OS - CPU SCHEDULER SYSTEM    
        + Custom Memory Allocator           
        + Enhanced File Server               
    =======================================
    )" << RESET << endl;
}

void printMenu() {
    cout << BOLD << CYAN << "\n=============== MAIN MENU ===============" << RESET << endl;
    cout << BOLD << "  1. Memory Allocator Test       " << RESET << endl;
    cout << BOLD << "  2. CPU Scheduler (FCFS)        " << RESET << endl;
    cout << BOLD << "  3. CPU Scheduler (SJF)         " << RESET << endl;
    cout << BOLD << "  4. CPU Scheduler (Priority)    " << RESET << endl;
    cout << BOLD << "  5. CPU Scheduler (Round Robin)  " << RESET << endl;
    cout << BOLD << "  6. Run All Schedulers          " << RESET << endl;
    cout << BOLD << "  7. Start File Server           " << RESET << endl;
    cout << BOLD << "  9. List Processes (API)        " << RESET << endl;
    cout << BOLD << "  8. Exit                        " << RESET << endl;
    cout << BOLD << CYAN << "==========================================" << RESET << endl;
    cout << BOLD << YELLOW << "Choose an option: " << RESET;
}

int main() {
    // Check if stdin is a pipe (API mode) - GetFileType for stdin
    HANDLE hStdin = GetStdHandle(STD_INPUT_HANDLE);
    DWORD fileType = GetFileType(hStdin);
    bool apiMode = (fileType == FILE_TYPE_PIPE);
    
    if (!apiMode) {
        printBanner();
    }
    
    CustomAllocator allocator;
    EnhancedScheduler scheduler;
    EnhancedFileServer fileServer;
    
    // Load sample processes
    scheduler.addProcess(1, 0, 5, 2);
    scheduler.addProcess(2, 1, 3, 1);
    scheduler.addProcess(3, 2, 8, 4);
    scheduler.addProcess(4, 3, 6, 3);
    scheduler.addProcess(5, 5, 4, 2);
    
    if (!apiMode) {
        cout << GREEN << "[OK] Loaded 5 sample processes" << RESET << endl;
    }
    
    while (true) {
        if (!apiMode) {
            printMenu();
        }
        int choice;
        if (!(cin >> choice)) {
            break;  // No more input in API mode
        }
        
        switch (choice) {
            case 1: {
                cout << BOLD << GREEN << "\n=== Memory Allocator Test ===" << RESET << endl;
                void* p1 = allocator.allocate(100);
                void* p2 = allocator.allocate(200);
                void* p3 = allocator.allocate(150);
                allocator.printStats();
                allocator.deallocate(p2);
                cout << GREEN << "[OK] Freed block P2" << RESET << endl;
                allocator.printStats();
                allocator.deallocate(p1);
                allocator.deallocate(p3);
                allocator.printStats();
                break;
            }
            case 2:
                scheduler.runFCFS();
                scheduler.printGantt();
                break;
            case 3:
                scheduler.runSJF();
                scheduler.printGantt();
                break;
            case 4:
                scheduler.runPriority();
                scheduler.printGantt();
                break;
            case 5:
                scheduler.runRoundRobin(2);
                scheduler.printGantt();
                break;
            case 6:
                scheduler.runFCFS();
                scheduler.printGantt();
                cout << endl;
                scheduler.runSJF();
                scheduler.printGantt();
                cout << endl;
                scheduler.runPriority();
                scheduler.printGantt();
                cout << endl;
                scheduler.runRoundRobin(2);
                scheduler.printGantt();
                break;
            case 7:
                if (fileServer.start()) {
                    fileServer.run();
                }
                break;
            case 9:
                // List processes in a parseable format for frontend
                cout << "PROCESSES_START" << endl;
                for (const auto& p : scheduler.getProcesses()) {
                    cout << "P" << p.id << ":" << p.arrival << ":" << p.burst << ":" << p.priority << endl;
                }
                cout << "PROCESSES_END" << endl;
                break;
            case 8:
                cout << BOLD << GREEN << "\nGoodbye!" << RESET << endl;
                return 0;
            default:
                cout << RED << "Invalid option!" << RESET << endl;
        }
    }
    
    return 0;
}
