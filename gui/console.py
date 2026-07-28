"""Output Console with ANSI color support and rich text display."""
import tkinter as tk
from tkinter import ttk
import re
import sys
import io
import threading
import queue
from contextlib import contextmanager
from gui.theme import *


class OutputConsole(ttk.Frame):
    """Rich output console with ANSI color support."""
    
    ANSI_COLORS = {
        # Standard colors
        '30': FG_DIM, '31': ERROR, '32': SUCCESS, '33': WARNING,
        '34': INFO, '35': "#c586c0", '36': "#4ec9b0", '37': FG,
        # Bright colors
        '90': FG_DIM, '91': "#f44747", '92': "#4ec990", '93': "#dcdcaa",
        '94': "#9cdcfe", '95': "#d4a5e5", '96': "#4ec9b0", '97': FG,
        # Background
        '40': CONSOLE_BG, '41': "#3a1a1a", '42': "#1a3a1a", '43': "#3a3a1a",
        '44': "#1a1a3a", '45': "#2d1a2d", '46': "#1a2d2d", '47': PANEL,
    }
    
    STYLES = {
        '0': {},      # Reset
        '1': {'font': ("Consolas", 10, "bold")},    # Bold
        '2': {},       # Dim
        '3': {'font': ("Consolas", 10, "italic")},  # Italic
        '4': {'font': ("Consolas", 10, "underline")}, # Underline
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.output_queue = queue.Queue()
        self.stdout_redirect = None
        self.stderr_redirect = None
        self._build_ui()
        self._process_queue()

    def _build_ui(self):
        """Build console UI."""
        # Toolbar
        toolbar = ttk.Frame(self, style="Console.TFrame")
        toolbar.pack(fill=tk.X, padx=4, pady=(4, 0))
        
        ttk.Label(toolbar, text="Console Output", style="Console.TLabel").pack(side=tk.LEFT)
        
        ttk.Button(toolbar, text="Clear", command=self.clear, width=8).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="Copy", command=self.copy_all, width=8).pack(side=tk.RIGHT, padx=2)
        
        # Auto-scroll checkbox
        self.auto_scroll = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Auto-scroll", variable=self.auto_scroll).pack(side=tk.RIGHT, padx=8)

        # Output area
        self.text = tk.Text(
            self,
            bg=CONSOLE_BG,
            fg=FG,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
            padx=8,
            pady=8,
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Scrollbar
        v_scroll = ttk.Scrollbar(self.text, orient=tk.VERTICAL, command=self.text.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=v_scroll.set)

        # Configure tags for ANSI colors
        self._setup_tags()

    def _setup_tags(self):
        """Configure text tags for ANSI colors."""
        for code, color in self.ANSI_COLORS.items():
            self.text.tag_configure(f"ansi_{code}", foreground=color)
        
        for code, style in self.STYLES.items():
            if style:
                self.text.tag_configure(f"style_{code}", **style)
        
        # Special tags
        self.text.tag_configure("stdout", foreground=FG)
        self.text.tag_configure("stderr", foreground=ERROR)
        self.text.tag_configure("system", foreground=INFO)
        self.text.tag_configure("prompt", foreground=ACCENT, font=("Consolas", 9, "bold"))
        self.text.tag_configure("result", foreground=SUCCESS)

    def _process_queue(self):
        """Process output queue from background threads."""
        try:
            while True:
                msg_type, content = self.output_queue.get_nowait()
                self._append(content, msg_type)
        except queue.Empty:
            pass
        self.after(50, self._process_queue)

    def _append(self, text: str, msg_type: str = "stdout"):
        """Append text to console with ANSI parsing."""
        self.text.config(state=tk.NORMAL)
        
        # Split by ANSI escape sequences
        parts = re.split(r'(\x1b\[[\d;]*m)', text)
        
        current_tags = []
        for part in parts:
            if part.startswith('\x1b['):
                # Parse ANSI code
                codes = part[2:-1].split(';')
                if codes == ['0'] or codes == ['']:
                    # Reset
                    current_tags = []
                else:
                    for code in codes:
                        if code in self.ANSI_COLORS:
                            current_tags.append(f"ansi_{code}")
                        elif code in self.STYLES:
                            current_tags.append(f"style_{code}")
            else:
                if part:
                    tags = tuple(current_tags) if current_tags else (msg_type,)
                    self.text.insert(tk.END, part, tags)
        
        self.text.config(state=tk.DISABLED)
        if self.auto_scroll.get():
            self.text.see(tk.END)

    def write(self, text: str, msg_type: str = "stdout"):
        """Thread-safe write to console."""
        self.output_queue.put((msg_type, text))

    def write_stdout(self, text: str):
        self.write(text, "stdout")

    def write_stderr(self, text: str):
        self.write(text, "stderr")

    def write_system(self, text: str):
        self.write(text, "system")

    def write_prompt(self, text: str):
        self.write(text, "prompt")

    def write_result(self, text: str):
        self.write(text, "result")

    def clear(self):
        """Clear console."""
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.config(state=tk.DISABLED)

    def copy_all(self):
        """Copy all console text to clipboard."""
        self.text.config(state=tk.NORMAL)
        content = self.text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(content)
        self.text.config(state=tk.DISABLED)

    def flush(self):
        """Flush method for file-like interface."""
        pass

    @contextmanager
    def redirect(self, stdout=True, stderr=True):
        """Context manager to redirect stdout/stderr."""
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        if stdout:
            sys.stdout = _Redirector(self, "stdout")
        if stderr:
            sys.stderr = _Redirector(self, "stderr")
        
        try:
            yield self
        finally:
            if stdout:
                sys.stdout = old_stdout
            if stderr:
                sys.stderr = old_stderr


class _Redirector:
    """File-like object to redirect stdout/stderr to console."""
    def __init__(self, console, msg_type):
        self.console = console
        self.msg_type = msg_type
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        if '\n' in text:
            lines = self.buffer.split('\n')
            self.buffer = lines[-1]
            for line in lines[:-1]:
                self.console.write(line + '\n', self.msg_type)
            if self.buffer:
                self.console.write(self.buffer, self.msg_type)

    def flush(self):
        if self.buffer:
            self.console.write(self.buffer, self.msg_type)
            self.buffer = ""


class ZapRunner:
    """Execute Zap code and capture output."""
    def __init__(self, console: OutputConsole):
        self.console = console
        self.running = False

    def run_file(self, filepath: str):
        """Run a Zap file."""
        import subprocess
        import os
        
        self.console.write_system(f">>> Running: {os.path.basename(filepath)}\n")
        
        def run():
            try:
                # Change to project root
                project_root = os.path.join(os.path.dirname(__file__), "..", "..")
                env = os.environ.copy()
                env['PYTHONPATH'] = os.path.join(project_root, "zap", "src") + os.pathsep + env.get('PYTHONPATH', '')
                
                proc = subprocess.Popen(
                    [sys.executable, "-m", "zap", "run", filepath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=project_root,
                    env=env
                )
                
                for line in iter(proc.stdout.readline, ''):
                    if line:
                        self.console.write(line, "stdout")
                
                proc.wait()
                if proc.returncode == 0:
                    self.console.write_result(f"\n>>> Exit code: {proc.returncode}\n")
                else:
                    self.console.write_stderr(f"\n>>> Exit code: {proc.returncode}\n")
                    
            except Exception as e:
                self.console.write_stderr(f"Error: {e}\n")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def run_code(self, code: str):
        """Run inline Zap code (writes to temp file)."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.zap', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            self.run_file(temp_path)
        finally:
            import os
            try:
                os.unlink(temp_path)
            except:
                pass

    def stop(self):
        """Stop running process."""
        self.running = False