#!/usr/bin/env python3
"""Port Killer GUI - Standalone graphical interface.

This is the GUI-only entry point that launches directly to the interface
without any command-line arguments or terminal window.
"""

from __future__ import annotations

import sys
from typing import List, Tuple, Iterable
from dataclasses import dataclass

try:
    import psutil
except ImportError as exc:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Missing Dependency",
        "psutil is required to use Port Killer.\n\n"
        "Please install it with:\npip install psutil"
    )
    sys.exit(1)

import tkinter as tk
from tkinter import messagebox, ttk


@dataclass
class ProcessSummary:
    pid: int
    name: str

    def __str__(self) -> str:
        return f"{self.name} (PID {self.pid})"


def _summarize(proc: psutil.Process) -> ProcessSummary:
    """Create a summary of a process."""
    name = None
    if hasattr(proc, "info"):
        name = proc.info.get("name")
    if not name:
        try:
            name = proc.name()
        except (psutil.Error, OSError):
            name = "<unknown>"
    return ProcessSummary(pid=proc.pid, name=name or "<unknown>")


def find_processes_on_port(port: int) -> List[psutil.Process]:
    """Return every process that has an INET connection bound to `port`."""
    matches: List[psutil.Process] = []
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            for conn in proc.net_connections(kind="inet"):
                if not conn.laddr:
                    continue
                if conn.laddr.port == port:
                    matches.append(proc)
                    break
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue
    return matches


def kill_processes(
    processes: Iterable[psutil.Process],
) -> Tuple[List[ProcessSummary], List[Tuple[ProcessSummary, str]]]:
    """Attempt to terminate each process and classify successes/failures."""
    killed: List[ProcessSummary] = []
    failed: List[Tuple[ProcessSummary, str]] = []
    for proc in processes:
        summary = _summarize(proc)
        try:
            proc.kill()
            killed.append(summary)
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess) as exc:
            failed.append((summary, str(exc)))
    return killed, failed


class PortKillerGUI:
    """Modern GUI for Port Killer application."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Port Killer")
        # Use pack to auto-size the window to fit content
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack()
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Port Killer",
            font=("Segoe UI", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Terminate processes using a specific port",
            font=("Segoe UI", 9)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Port input section
        port_frame = ttk.Frame(main_frame)
        port_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Label(
            port_frame,
            text="Port Number:",
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        self.port_entry = ttk.Entry(port_frame, width=15, font=("Segoe UI", 10))
        self.port_entry.grid(row=0, column=1)
        self.port_entry.focus_set()
        
        # Bind Enter key to kill action
        self.port_entry.bind('<Return>', lambda e: self.on_kill())
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.scan_button = ttk.Button(
            button_frame,
            text="Scan Port",
            command=self.on_scan,
            width=15
        )
        self.scan_button.grid(row=0, column=0, padx=5)
        
        self.kill_button = ttk.Button(
            button_frame,
            text="Kill Process",
            command=self.on_kill,
            width=15
        )
        self.kill_button.grid(row=0, column=1, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Footer
        footer_label = ttk.Label(
            main_frame,
            text="Note: Administrator privileges may be required",
            font=("Segoe UI", 8),
            foreground="gray"
        )
        footer_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
    
    def on_scan(self):
        """Scan for processes on the specified port without killing them."""
        port_value = self.port_entry.get().strip()
        if not port_value:
            messagebox.showerror("Error", "Please enter a port number.")
            return
        
        try:
            port = int(port_value)
            if port < 1 or port > 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid port number: {e}")
            return
        
        self.status_label.config(text=f"Scanning port {port}...")
        self.root.update()
        
        try:
            processes = find_processes_on_port(port)
            
            if not processes:
                self.status_label.config(text="")
                messagebox.showinfo("Scan Result", f"No processes are listening on port {port}.")
                return
            
            # Show process list
            process_list = "\n".join(f"• {_summarize(p)}" for p in processes)
            self.status_label.config(text="")
            messagebox.showinfo(
                "Processes Found",
                f"Found {len(processes)} process(es) on port {port}:\n\n{process_list}"
            )
        except Exception as e:
            self.status_label.config(text="")
            messagebox.showerror("Error", f"An error occurred while scanning:\n{e}")
    
    def on_kill(self):
        """Kill all processes on the specified port."""
        port_value = self.port_entry.get().strip()
        if not port_value:
            messagebox.showerror("Error", "Please enter a port number.")
            return
        
        try:
            port = int(port_value)
            if port < 1 or port > 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid port number: {e}")
            return
        
        self.status_label.config(text=f"Searching for processes on port {port}...")
        self.root.update()
        
        try:
            processes = find_processes_on_port(port)
            
            # Reset Port Label
            self.port_entry.delete(0, tk.END)

            if not processes:
                self.status_label.config(text="")
                messagebox.showinfo("Info", f"No processes are listening on port {port}.")
                return
            
            # Kill processes directly without confirmation
            self.status_label.config(text=f"Terminating {len(processes)} process(es)...")
            self.root.update()
            
            killed, failed = kill_processes(processes)
            
            messages = []
            if killed:
                lines = "\n".join(f"✓ {summary}" for summary in killed)
                messages.append(f"Successfully killed:\n{lines}")
            if failed:
                lines = "\n".join(f"✗ {summary}: {error}" for summary, error in failed)
                messages.append(f"Failed to kill:\n{lines}")
            
            self.status_label.config(text=f"Operation complete ({len(killed)} killed, {len(failed)} failed)")
            
            if messages:
                if failed:
                    messagebox.showwarning("Result", "\n\n".join(messages))
                else:
                    messagebox.showinfo("Result", "\n\n".join(messages))
            else:
                messagebox.showinfo("Result", "No action taken.")
                
        except Exception as e:
            self.status_label.config(text="")
            messagebox.showerror("Error", f"An error occurred:\n{e}")
    
    def run(self):
        """Start the GUI event loop."""
        self.root.mainloop()


def main():
    """Launch the GUI application."""
    app = PortKillerGUI()
    app.run()


if __name__ == "__main__":
    main()


