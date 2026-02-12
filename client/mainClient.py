"""
Advanced OS Project - Enhanced GUI Frontend
Fully connected to backend C++ for CPU scheduling and memory allocation
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import sys
import threading
import json


class CPUSchedulerGUI:
    """Modern GUI for CPU Scheduling Algorithms - Connected to Backend"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced OS - CPU Scheduler & Memory Allocator")
        self.root.geometry("1200x850")
        self.root.minsize(1000, 700)
        
        # Colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#27ae60',
            'warning': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#1a252f',
            'text': '#2c3e50',
            'bg': '#f8f9fa',
            'success': '#27ae60',
            'info': '#3498db',
            'purple': '#9b59b6',
            'orange': '#e67e22'
        }
        
        # Backend connection
        self.backend_process = None
        self.backend_ready = False
        self.processes_from_backend = []
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_header()
        self.create_main_container()
        
        # Start backend connection
        self.start_backend_connection()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], 
                       foreground=self.colors['text'], font=('Segoe UI', 10))
        style.configure('TLabelframe', background=self.colors['bg'],
                       foreground=self.colors['primary'])
        style.configure('TLabelframe.Label', background=self.colors['bg'],
                       foreground=self.colors['primary'], font=('Segoe UI', 11, 'bold'))
        
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['secondary'], foreground='white')
        style.map('Primary.TButton', background=[('active', '#2980b9')])
        
        style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['accent'], foreground='white')
        style.map('Success.TButton', background=[('active', '#1e8449')])
        
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['purple'], foreground='white')
        style.map('Accent.TButton', background=[('active', '#8e44ad')])
        
        style.configure('Warning.TButton', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['orange'], foreground='white')
        style.map('Warning.TButton', background=[('active', '#d35400')])
        
        style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['warning'], foreground='white')
        style.map('Danger.TButton', background=[('active', '#c0392b')])
        
        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[12, 6])
        
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=28,
                       background='white', fieldbackground='white')
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['primary'], foreground='white')
        
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="OS Nexus Studio - CPU Scheduler & Memory Allocator",
                              font=('Segoe UI', 26, 'bold'), bg=self.colors['primary'], fg='white')
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(header_frame,
                                  text="CPU Scheduler | Memory Allocator | Backend Connected",
                                  font=('Segoe UI', 11), bg=self.colors['primary'], fg='#bdc3c7')
        subtitle_label.pack(pady=(0, 20))
        
    def create_main_container(self):
        """Create main content area"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right panel
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Backend status
        self.create_backend_status(left_panel)
        
        # Process management
        self.create_process_section(left_panel)
        
        # Algorithm buttons
        self.create_algorithm_section(left_panel)
        
        # Enhanced backend controls
        self.create_enhanced_section(left_panel)
        
        # Results
        self.create_results_section(right_panel)
        
        # Process list
        self.create_process_list(right_panel)
        
    def create_backend_status(self, parent):
        """Create backend connection status"""
        status_frame = ttk.LabelFrame(parent, text="  Backend Connection Status  ", padding=10)
        status_frame.pack(fill='x', pady=(0, 15))
        
        self.status_label = tk.Label(status_frame, text="Connecting to backend...",
                                    font=('Segoe UI', 10), bg=self.colors['bg'],
                                    fg=self.colors['warning'])
        self.status_label.pack(anchor='w')
        
        # Status indicator
        self.status_indicator = tk.Canvas(status_frame, width=20, height=20, bg=self.colors['bg'],
                                         highlightthickness=0)
        self.status_indicator.pack(side='right')
        self.status_indicator.create_oval(2, 2, 18, 18, fill=self.colors['warning'], outline='')
        
    def create_process_section(self, parent):
        """Create process input section"""
        input_frame = ttk.LabelFrame(parent, text="  Process Management (From Backend)  ", padding=15)
        input_frame.pack(fill='x', pady=(0, 15))
        
        info_label = tk.Label(input_frame, 
                             text="Processes are loaded automatically from the enhanced backend.\n"
                                  "The backend comes pre-loaded with 5 sample processes.",
                             font=('Segoe UI', 9), bg=self.colors['bg'],
                             fg=self.colors['text'], justify='left')
        info_label.pack(anchor='w', pady=(0, 10))
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame, text="Load Processes from Backend", 
                   command=self.load_processes_from_backend,
                   style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="Refresh Process List", 
                   command=self.refresh_process_list,
                   style='Primary.TButton').pack(side='left', padx=5)
        
    def create_algorithm_section(self, parent):
        """Create algorithm buttons"""
        algo_frame = ttk.LabelFrame(parent, text="  Scheduling Algorithms  ", padding=15)
        algo_frame.pack(fill='x', pady=(0, 15))
        
        buttons = [
            ("FCFS", self.run_fcfs_backend, '#3498db'),
            ("SJF", self.run_sjf_backend, '#9b59b6'),
            ("Priority", self.run_priority_backend, '#e67e22'),
            ("Round Robin", self.run_rr_backend, '#1abc9c'),
        ]
        
        btn_frame = ttk.Frame(algo_frame)
        btn_frame.pack(fill='x')
        
        for i, (text, cmd, color) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=text, command=cmd, style='Primary.TButton')
            btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            btn_frame.columnconfigure(i, weight=1)
        
        ttk.Button(algo_frame, text="Run All Algorithms via Backend", 
                   command=self.run_all_backend, style='Accent.TButton').pack(fill='x', pady=(10, 0))
        
    def create_enhanced_section(self, parent):
        """Create enhanced backend controls"""
        enhanced_frame = ttk.LabelFrame(parent, text="  Enhanced Backend Features  ", padding=15)
        enhanced_frame.pack(fill='x', pady=(0, 15))
        
        # Info
        info_text = "Run enhanced backend features:\n" \
                   "- Memory Allocator Test: Tests the custom 1MB memory allocator\n" \
                   "- File Server: Starts TCP server on port 9090"
        info_label = tk.Label(enhanced_frame, text=info_text,
                             font=('Segoe UI', 9), bg=self.colors['bg'],
                             fg=self.colors['text'], justify='left')
        info_label.pack(anchor='w', pady=(0, 10))
        
        btn_frame = ttk.Frame(enhanced_frame)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame, text="Run Memory Test", 
                   command=self.run_memory_test_backend,
                   style='Warning.TButton').pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="Start File Server", 
                   command=self.start_file_server_backend,
                   style='Primary.TButton').pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="Open Backend Terminal", 
                   command=self.open_backend_terminal,
                   style='Accent.TButton').pack(side='left', padx=5)
        
    def create_results_section(self, parent):
        """Create results display area"""
        results_frame = ttk.LabelFrame(parent, text="  Results from Backend  ", padding=15)
        results_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.result_tabs = {}
        tabs = ['FCFS', 'SJF', 'Priority', 'Round Robin', 'Memory', 'File Server']
        
        for algo in tabs:
            tab = ttk.Frame(self.results_notebook)
            self.results_notebook.add(tab, text=f" {algo} ")
            
            text_widget = scrolledtext.ScrolledText(tab, wrap='word',
                                                   font=('Consolas', 10),
                                                   bg='white', fg=self.colors['text'])
            text_widget.pack(fill='both', expand=True, padx=5, pady=5)
            self.result_tabs[algo] = text_widget
            
        # Gantt chart
        gantt_frame = ttk.LabelFrame(parent, text="  Gantt Chart Visualization  ", padding=15)
        gantt_frame.pack(fill='x')
        
        self.gantt_canvas = tk.Canvas(gantt_frame, height=150, bg='white',
                                     highlightthickness=1,
                                     highlightbackground=self.colors['secondary'])
        self.gantt_canvas.pack(fill='x', pady=5)
        
    def create_process_list(self, parent):
        """Create process list table"""
        list_frame = ttk.LabelFrame(parent, text="  Backend Processes  ", padding=15)
        list_frame.pack(fill='x')
        
        columns = ('pid', 'arrival', 'burst', 'priority')
        self.process_tree = ttk.Treeview(list_frame, columns=columns,
                                        show='headings', height=6)
        
        self.process_tree.heading('pid', text='Process ID')
        self.process_tree.heading('arrival', text='Arrival Time')
        self.process_tree.heading('burst', text='Burst Time')
        self.process_tree.heading('priority', text='Priority')
        
        self.process_tree.column('pid', width=100, anchor='center')
        self.process_tree.column('arrival', width=120, anchor='center')
        self.process_tree.column('burst', width=120, anchor='center')
        self.process_tree.column('priority', width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical',
                                command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side='left', fill='x', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Status label
        self.process_count_label = tk.Label(list_frame, text="No processes loaded",
                                           font=('Segoe UI', 9), bg=self.colors['bg'],
                                           fg=self.colors['text'])
        self.process_count_label.pack(anchor='w', pady=(5, 0))
        
    # ========== BACKEND CONNECTION METHODS ==========
    
    def start_backend_connection(self):
        """Start backend connection in background"""
        self.status_label.config(text="Initializing backend connection...", fg=self.colors['warning'])
        threading.Thread(target=self._backend_thread, daemon=True).start()
        
    def _backend_thread(self):
        """Backend connection thread"""
        import time
        time.sleep(1)  # Simulate connection
        self.root.after(0, self._on_backend_ready)
        
    def _on_backend_ready(self):
        """Called when backend is ready"""
        self.backend_ready = True
        self.status_label.config(text="✓ Connected to Enhanced Backend", fg=self.colors['success'])
        self.status_indicator.delete("all")
        self.status_indicator.create_oval(2, 2, 18, 18, fill=self.colors['success'], outline='')
        self.load_processes_from_backend()
        
    def load_processes_from_backend(self):
        """Load REAL processes from the enhanced backend server"""
        try:
            # Get executable path
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            exe_path = os.path.join(base_path, '..', 'server', 'main_system.exe')
            exe_path = os.path.normpath(exe_path)
            
            if not os.path.exists(exe_path):
                self.status_label.config(text="⚠ Backend not found", fg=self.colors['warning'])
                return
            
            # Run backend with option 9 to get processes list
            input_data = "9\n8\n"
            
            process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            stdout, stderr = process.communicate(input=input_data, timeout=10)
            
            # Parse the output to extract processes
            self.processes_from_backend = []
            
            in_processes = False
            for line in stdout.split('\n'):
                line = line.strip()
                if line == 'PROCESSES_START':
                    in_processes = True
                    continue
                if line == 'PROCESSES_END':
                    break
                if in_processes and line:
                    # Format: P<id>:<arrival>:<burst>:<priority>
                    try:
                        parts = line.split(':')
                        if len(parts) == 4:
                            process_id = parts[0]
                            arrival = int(parts[1])
                            burst = int(parts[2])
                            priority = int(parts[3])
                            self.processes_from_backend.append({
                                'id': process_id,
                                'arrival': arrival,
                                'burst': burst,
                                'priority': priority
                            })
                    except (ValueError, IndexError):
                        continue
            
            if self.processes_from_backend:
                self.update_process_list()
                self.status_label.config(
                    text=f"✓ Loaded {len(self.processes_from_backend)} processes from backend", 
                    fg=self.colors['success']
                )
            else:
                self.status_label.config(text="⚠ No processes found in backend", fg=self.colors['warning'])
                
        except Exception as e:
            self.status_label.config(text=f"⚠ Error loading processes: {str(e)}", fg=self.colors['warning'])
        
    def refresh_process_list(self):
        """Refresh process list from backend"""
        self.load_processes_from_backend()
        
    def update_process_list(self):
        """Update the process treeview"""
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
            
        for p in self.processes_from_backend:
            self.process_tree.insert('', 'end', values=(p['id'], p['arrival'], p['burst'], p['priority']))
            
        self.process_count_label.config(
            text=f"Showing {len(self.processes_from_backend)} processes from enhanced backend")
    
    def prepare_backend_input(self):
        """Prepare input for backend based on loaded processes"""
        n = len(self.processes_from_backend)
        input_str = str(n) + "\n"
        
        for p in sorted(self.processes_from_backend, key=lambda x: x['arrival']):
            input_str += f"{p['arrival']} {p['burst']} {p['priority']}\n"
            
        return input_str
        
    def run_fcfs_backend(self):
        """Run FCFS via backend"""
        self.run_algorithm_backend(2, 'FCFS')
        
    def run_sjf_backend(self):
        """Run SJF via backend"""
        self.run_algorithm_backend(3, 'SJF')
        
    def run_priority_backend(self):
        """Run Priority via backend"""
        self.run_algorithm_backend(4, 'Priority')
        
    def run_rr_backend(self):
        """Run Round Robin via backend"""
        self.run_algorithm_backend(5, 'Round Robin')
        
    def run_all_backend(self):
        """Run all algorithms via backend"""
        self.run_algorithm_backend(6, 'All')
        
    def run_algorithm_backend(self, option, tab_name):
        """Run algorithm by sending input to backend"""
        try:
            # Get executable path
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            exe_path = os.path.join(base_path, '..', 'server', 'main_system.exe')
            exe_path = os.path.normpath(exe_path)
            
            if not os.path.exists(exe_path):
                messagebox.showerror("Error", f"Backend not found: {exe_path}")
                return
            
            # Prepare input: select option, then 8 to exit
            input_data = f"{option}\n8\n"
            
            # Run backend
            process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            stdout, stderr = process.communicate(input=input_data, timeout=10)
            
            if stderr:
                messagebox.showwarning("Warning", f"Backend stderr: {stderr}")
            
            # Display results
            self.display_backend_results(tab_name, stdout)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run backend: {str(e)}")
            
    def display_backend_results(self, tab_name, output):
        """Display results from backend"""
        widget = self.result_tabs[tab_name]
        widget.delete('1.0', 'end')
        widget.insert('end', output)
        
        # Select the tab
        algo_index = {'FCFS': 0, 'SJF': 1, 'Priority': 2, 'Round Robin': 3, 'All': 0}
        if tab_name in algo_index:
            self.results_notebook.select(algo_index[tab_name])
            
        # Draw Gantt chart if present
        self.draw_gantt_from_output(output)
        
    def draw_gantt_from_output(self, output):
        """Draw Gantt chart from backend output"""
        self.gantt_canvas.delete("all")
        
        lines = output.split('\n')
        gantt_data = []
        
        for line in lines:
            if '->' in line and 'P' in line:
                # Parse: "P1: 0 -> 5"
                try:
                    parts = line.split(':')[1].strip()
                    times = parts.split('->')
                    pid = line.split(':')[0].strip()
                    start = int(times[0].strip())
                    end = int(times[1].strip())
                    gantt_data.append({'pid': pid, 'start': start, 'end': end})
                except:
                    pass
        
        if not gantt_data:
            return
            
        # Calculate dimensions
        max_time = max(d['end'] for d in gantt_data)
        canvas_width = self.gantt_canvas.winfo_width() - 100
        canvas_height = 120
        
        if max_time == 0:
            return
            
        scale = canvas_width / max_time if max_time > 0 else 1
        bar_height = 40
        start_y = (canvas_height - bar_height) / 2
        
        # Draw timeline
        self.gantt_canvas.create_line(50, canvas_height/2 + 20, 50 + canvas_width, 
                                     canvas_height/2 + 20, fill=self.colors['secondary'], width=2)
        
        # Draw blocks
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        for i, data in enumerate(gantt_data):
            x1 = 50 + data['start'] * scale
            x2 = 50 + data['end'] * scale
            color = colors[i % len(colors)]
            
            # Draw block
            self.gantt_canvas.create_rectangle(x1, start_y, x2, start_y + bar_height,
                                             fill=color, outline='')
            # Draw PID
            self.gantt_canvas.create_text((x1 + x2)/2, start_y + bar_height/2,
                                         text=data['pid'], fill='white', font=('Arial', 10, 'bold'))
            
            # Draw start time
            self.gantt_canvas.create_text(x1, start_y + bar_height + 15,
                                         text=str(data['start']), font=('Arial', 8))
            
        # Draw end time
        if gantt_data:
            self.gantt_canvas.create_text(50 + max_time * scale, start_y + bar_height + 15,
                                         text=str(max_time), font=('Arial', 8))
        
    def run_memory_test_backend(self):
        """Run memory allocator test via backend"""
        self.run_algorithm_backend(1, 'Memory')
        
    def start_file_server_backend(self):
        """Start file server via backend"""
        self.run_algorithm_backend(7, 'File Server')
        
    def open_backend_terminal(self):
        """Open backend in new terminal window"""
        try:
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            exe_path = os.path.join(base_path, '..', 'server', 'main_system.exe')
            exe_path = os.path.normpath(exe_path)
            
            if not os.path.exists(exe_path):
                messagebox.showerror("Error", f"Backend not found: {exe_path}")
                return
            
            # Open in new command prompt
            subprocess.Popen(['cmd', '/k', exe_path])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open backend: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
