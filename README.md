# OS-Nexus-Studio

OS Nexus Studio is an educational operating system simulation platform combining a high-performance C++ backend with a Python GUI frontend. It demonstrates CPU scheduling algorithms (FCFS, SJF, Priority, Round Robin) alongside a multithreaded TCP file server for concurrent client handling. Designed for clarity and learning, the project visualizes process execution, networking, and synchronization concepts in a practical environment 🚀, making core OS concepts easier to understand and experiment with 🧠.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
   - [CPU Scheduling](#cpu-scheduling)
   - [Memory Allocator](#memory-allocator)
   - [File Server](#file-server)
3. [Getting Started](#getting-started)
4. [Project Structure](#project-structure)
5. [Usage Guide](#usage-guide)
   - [GUI Frontend](#gui-frontend)
   - [Backend Terminal](#backend-terminal)
   - [API Mode](#api-mode)
6. [Architecture](#architecture)
7. [Building from Source](#building-from-source)
8. [API Reference](#api-reference)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)


## Overview

OS-Nexus-Studio provides hands-on experience with core operating system concepts through an interactive simulation platform. The system demonstrates:

- **CPU Scheduling** - Four scheduling algorithms with visual output and metrics
- **Memory Management** - Custom block-based memory allocator
- **Networking** - Multi-client TCP file server

The platform bridges theory and practice by allowing users to experiment with OS concepts in a controlled environment.


## Features

### CPU Scheduling

Four scheduling algorithms with comprehensive metrics:

| Algorithm | Type | Description | Time Quantum |
|-----------|------|-------------|-------------|
| FCFS | Non-preemptive | First Come First Serve | - |
| SJF | Non-preemptive | Shortest Job First | - |
| Priority | Non-preemptive | Priority-based scheduling | - |
| Round Robin | Preemptive | Time-slice based | 2 units |

**Metrics Provided:**
- Process execution timeline
- Completion time (CT)
- Turnaround time (TAT)
- Waiting time (WT)
- Average statistics
- Gantt chart visualization

### Memory Allocator

Custom block-based allocator implementing:

- **1MB Heap** - Pre-allocated virtual memory
- **First-Fit Strategy** - Finds first suitable block
- **Block Splitting** - Divides large blocks for efficiency
- **Coalescing** - Merges adjacent free blocks
- **Fragmentation Tracking** - Real-time statistics

**Statistics:**
- Total heap size
- Allocated memory
- Free memory
- Fragmentation percentage

### File Server

Multi-client TCP server on port 9090:

| Command | Description | Usage |
|---------|-------------|-------|
| LIST | List available files | `LIST` |
| GET | Download file contents | `GET <filename>` |
| INFO | Get file size | `INFO <filename>` |

**Features:**
- Concurrent client handling
- Real-time connection status
- Binary and text file support


## Getting Started

### Prerequisites

- Python 3.8+ (for GUI frontend)
- MinGW-w64 with g++ (for backend compilation)
- Windows 10/11

### Quick Start

#### GUI Frontend (Recommended)
```cmd
python client/mainClient.py
```

#### Backend Terminal
```cmd
server/main_system.exe
```


## Project Structure

```
OS-Nexus-Studio/
├── README.md                 # Documentation
├── LICENSE                    # MIT License
├── .gitignore                # Git ignore rules
├── client/
│   └── mainClient.py         # GUI Frontend (Python/tkinter)
└── server/
    ├── main_system.cpp       # Main backend (C++)
    ├── main_system.exe       # Compiled executable
    ├── scheduler.cpp         # Standalone scheduler
    ├── scheduler.exe         # Compiled executable
    ├── file_server.cpp       # Standalone file server
    └── file_server.exe       # Compiled executable
```


## Usage Guide

### GUI Frontend

#### Adding Processes

1. Enter process details:
   - **Process ID** - Unique identifier (e.g., P1, P2)
   - **Arrival Time** - When process arrives
   - **Burst Time** - CPU time required
   - **Priority** - Scheduling priority (1-10)

2. Click "Add Process"

3. Manage processes:
   - "Clear All" - Remove all processes
   - "Load Sample Data" - Restore default 5 processes
   - "Refresh Process List" - Reload from backend

#### Running Algorithms

1. Select an algorithm:
   - FCFS
   - SJF
   - Priority
   - Round Robin
   - "Run All Algorithms" - Compare all

2. View results in tabbed panels

3. Gantt chart displays execution timeline

#### Backend Features

- **Run Memory Test** - Test custom allocator
- **Start File Server** - Launch TCP server
- **Open Backend Terminal** - Interactive mode

### Backend Terminal

Run `server/main_system.exe` for interactive mode:

```
=============== MAIN MENU ===============
  1. Memory Allocator Test
  2. CPU Scheduler (FCFS)
  3. CPU Scheduler (SJF)
  4. CPU Scheduler (Priority)
  5. CPU Scheduler (Round Robin)
  6. Run All Schedulers
  7. Start File Server
  9. List Processes (API)
 10. Add Process (API)
 11. Clear All Processes (API)
 12. Load Sample Processes (API)
  8. Exit
```

### API Mode

The backend supports programmatic access via pipe I/O:

**Input Format:**
```
<num_processes>
<arrival_time> <burst_time> <priority>
...
<algorithm_option>
8
```

**Example (FCFS with 3 processes):**
```
3
0 5 2
1 3 1
2 8 4
2
8
```

**Response Format:**
```
--- Running FCFS Scheduler ---
P1: 0 -> 5 | Waiting: 0
P2: 5 -> 8 | Waiting: 4
...

--- Scheduling Statistics ---
ID    AT    BT    CT    TAT    WT
----------------------------------------
P1    0     5     5     5      0
...

Avg Waiting Time: 3.33
Avg Turnaround Time: 7.33
```


## Architecture

### System Components

```
┌─────────────────────────────────────────┐
│           GUI Frontend                   │
│         (Python/tkinter)                 │
│                                         │
│  - Process management UI                 │
│  - Algorithm selection                   │
│  - Result visualization                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           Backend (C++)                  │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │    Custom Memory Allocator       │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │    CPU Scheduler                 │    │
│  │  - FCFS  - SJF                  │    │
│  │  - Priority  - Round Robin       │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │    TCP File Server               │    │
│  │  - LIST  - GET  - INFO          │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Data Flow

1. User creates processes in GUI
2. Frontend sends data to backend via pipe
3. Backend computes scheduling results
4. Results returned and visualized in GUI


## Building from Source

### Main Backend (Required)

```cmd
g++ -std=c++11 -o server/main_system server/main_system.cpp -lws2_32
```

### Standalone Scheduler (Optional)

```cmd
g++ -std=c++11 -o server/scheduler server/scheduler.cpp
```

### Standalone File Server (Optional)

```cmd
g++ -o server/file_server server/file_server.cpp -lws2_32
```


## API Reference

### Process Structure

```cpp
struct Process {
    int id;           // Process identifier
    int arrival;      // Arrival time
    int burst;         // Burst time (CPU required)
    int priority;      // Scheduling priority
    int completion;    // Completion time
    int turnaround;   // Turnaround time
    int waiting;      // Waiting time
};
```

### Scheduler Methods

| Method | Description |
|--------|-------------|
| `addProcess()` | Add a process to the queue |
| `runFCFS()` | Execute FCFS scheduling |
| `runSJF()` | Execute SJF scheduling |
| `runPriority()` | Execute Priority scheduling |
| `runRoundRobin(q)` | Execute Round Robin with quantum q |
| `getProcesses()` | Get all processes |
| `clear()` | Clear all processes |

### Memory Allocator Methods

| Method | Description |
|--------|-------------|
| `allocate(size)` | Allocate memory block |
| `deallocate(ptr)` | Free allocated block |
| `printStats()` | Print allocation statistics |

## Examples

### Example 1: FCFS Scheduling

**Input:**
```
3
0 5 2
1 3 1
2 8 4
2
8
```

**Output:**
```
--- Running FCFS Scheduler ---
P1: 0 -> 5 | Waiting: 0
P2: 5 -> 8 | Waiting: 4
P3: 8 -> 16 | Waiting: 6

--- Scheduling Statistics ---
ID    AT    BT    CT    TAT    WT
----------------------------------------
P1    0     5     5     5      0
P2    1     3     8     7      4
P3    2     8     16    14     6
----------------------------------------
Avg Waiting Time: 3.33
Avg Turnaround Time: 8.67
```

### Example 2: Memory Allocation Test

**Output:**
```
=== Memory Allocator Test ===
=== Memory Allocator Stats ===
Total Heap Size: 1024 KB
Allocated: 0 KB
Free: 1024 KB
Fragmentation: 0.00%
[OK] Freed block P2
=== Memory Allocator Stats ===
Total Heap Size: 1024 KB
Allocated: 0 KB
Free: 1024 KB
Fragmentation: 0.00%
```


## Troubleshooting

| Issue | Solution |
|-------|----------|
| g++ not found | Install MinGW-w64 and add to PATH. Restart terminal after installation. |
| Python not found | Reinstall Python with "Add to PATH" option enabled. |
| GUI won't start | Ensure tkinter is installed: `pip install tk` |
| Port 9090 in use | Close any running file server or change PORT in source code |
| Backend crashes | Ensure no other instance is running. Check Task Manager. |


## License

MIT License - Open-source project for educational purposes.

Copyright (c) 2026 Ujjwal Saini