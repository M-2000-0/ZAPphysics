"""
ZapPhysics Professional — Console
Rich output console with ANSI colors, filtering, and advanced features.
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional, Callable, List, Tuple
import re
import queue
import threading
import sys
from contextlib import contextmanager
import time


# ANSI Color mapping
ANSI_COLORS = {
    '30': "#6e7681", '31': "#f85149", '32': "#3fb950", '33': "#d29922",
    '34': "#58a6ff", '35': "#c586c0", '36': "#4ec9b0", '37': "#e6edf3",
    '90': "#6e7681", '91': "#ff7b72", '92': "#3fb950", '93': "#d29922",
    '94': "#9cdcfe", '95': "#c586c0", '96': "#4ec9b0", '97': "#e6edf3",
    '40': "#0d1117", '41': "#3a1d1d", '42': "#1a3a1a", '43': "#3a3a1a",
    '44': "#1a1a3a", '45': "#2d1a2d", '46': "#1a2d2d", '47': "#161b22",
}

ANSI_STYLES = {
    '0': {}, '1': {"font": ("JetBrains Mono", 11, "bold")},
    '3': {"font": ("JetBrains Mono", 11, "italic")},
    '4': {"font": ("JetBrains Mono", 11, "underline")},
}


class OutputConsole(ctk.CTkFrame):
    """Professional output console with ANSI support, filtering, and rich features."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#0d1117", corner_radius=8, border_width=1, border_color="#30363d", **kwargs)
        
        self.output_queue = queue.Queue()
        self.max_lines = 10000
        self._filter_level = "all"
        self._search_text = ""
        self._auto_scroll = True
        self._timestamps = False
        self._paused = False
        
        self._build_ui()
        self.after(30, self._process_queue)
        
    def _build_ui(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent", height=36)
        toolbar.pack(fill="x", padx=8, pady=(8, 0))
        toolbar.pack_propagate(False)
        toolbar.grid_columnconfigure(1, weight=1)
        
        # Title
        ctk.CTkLabel(
            toolbar, text="Console",
            font=ctk.CTkFont(weight="bold", size=13),
            text_color="#e6edf3"
        ).pack(side="left", padx=12)
        
        # Filter
        self.filter_var = ctk.StringVar(value="All")
        filter_combo = ctk.CTkComboBox(
            toolbar, values=["All", "Output", "Errors", "System", "Results"],
            variable=self.filter_var, width=100,
            command=self._on_filter_change
        )
        self.filter_var.trace_add("write", self._filter)
        filter_combo.pack(side="right", padx=8)
        
        ctk.CTkLabel(self, text="Filter:", font=ctk.CTkFont(size=11)).place(relx=0.75, rely=0.5, anchor="e")
        
        # Search
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter)
        search_entry = ctk.CTkEntry(
            self, textvariable=self.search_var, placeholder_text="🔍 Search...",
            width=150, height=28, font=ctk.CTkFont(size=11)
        )
        search_entry.place(relx=0.98, rely=0.5, anchor="e")
        
        # Control buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.place(relx=1.0, rely=0.5, anchor="e", x=-150, y=0)
        
        from .widgets import ProButton
        ProButton(self, text="Clear", variant="ghost", width=70, command=self.clear).place(relx=0.85, rely=0.5, anchor="e")
        ProButton(self, text="Copy", variant="ghost", width=70, command=self.copy_all).place(relx=0.92, rely=0.5, anchor="e")
        
        # Auto-scroll toggle
        toggle_frame = ctk.CTkFrame(self, fg_color="transparent")
        toggle_frame.pack(side="right", padx=4)
        
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(self, text="Auto-scroll", variable=self.auto_scroll_var, width=80).pack(side="right", padx=8)
        
        # Text area
        self.text = tk.Text(
            self,
            bg="#0d1117",
            fg="#e6edf3",
            font=("JetBrains Mono", 11) if self._font_exists("JetBrains Mono") else ("Consolas", 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
            padx=12, pady=10,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # Scrollbar
        v_scroll = ctk.CTkScrollbar(self, command=self.text.yview)
        v_scroll.pack(side="right", fill="y", padx=(0, 8), pady=(0, 8))
        self.text.configure(yscrollcommand=v_scroll.set)
        
        # ANSI tag setup
        self._setup_tags()
        
    def _font_exists(self, name: str) -> bool:
        import tkinter.font as tkfont
        return name in tkfont.families()
        
    def _setup_tags(self):
        """Configure text tags for ANSI colors and styles."""
        for code, color in ANSI_COLORS.items():
            self.text.tag_configure(f"ansi_{code}", foreground=color)
            
        for code, style in ANSI_STYLES.items():
            if style:
                self.text.tag_configure(f"style_{code}", **style)
                
        # Custom tags
        self.text.tag_configure("stdout", foreground="#e6edf3")
        self.text.tag_configure("stderr", foreground="#f85149")
        self.text.tag_configure("system", foreground="#58a6ff")
        self.text.tag_configure("success", foreground="#3fb950")
        self.text.tag_configure("warning", foreground="#d29922")
        self.text.tag_configure("error", foreground="#f85149")
        self.text.tag_configure("info", foreground="#58a6ff")
        self.text.tag_configure("prompt", foreground="#58a6ff", font=("JetBrains Mono", 11, "bold"))
        self.text.tag_configure("result", foreground="#3fb950")
        self.text.tag_configure("timestamp", foreground="#6e7681")
        self.text.tag_configure("search_match", background="#264f78", foreground="#ffffff")
        
    def write(self, text: str, msg_type: str = "stdout"):
        """Thread-safe write to console."""
        if not self._paused:
            self.output_queue.put((msg_type, text))
            
    def _process_queue(self):
        """Process output queue."""
        try:
            while True:
                msg_type, content = self.output_queue.get_nowait()
                self._append(content, msg_type)
        except queue.Empty:
            pass
        self.after(30, self._process_queue)
        
    def _append(self, text: str, msg_type: str = "stdout"):
        """Append text with ANSI parsing."""
        if self._paused:
            return
            
        # Apply filter
        if self._filter_level != "all":
            type_map = {"Output": "stdout", "Errors": "stderr", "System": "system", "Results": "result"}
            if msg_type not in [type_map.get(self._filter_level, ""), "system"]:
                return
                
        # Check search filter
        if self._search_text and self._search_text.lower() not in text.lower():
            return
            
        self.text.configure(state=tk.NORMAL)
        
        # Add timestamp if enabled
        if self._timestamps:
            ts = time.strftime("%H:%M:%S")
            self.text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] ", ("timestamp",))
            
        # Parse ANSI escape sequences
        parts = re.split(r'(\x1b\[[\d;]*m)', text)
        
        current_tags = ()
        for part in parts:
            if part.startswith('\x1b['):
                codes = part[2:-1].split(';')
                if codes == ['0'] or codes == ['']:
                    current_tags = ()
                else:
                    tags = []
                    for code in codes:
                        if code in ANSI_COLORS:
                            tags.append(f"ansi_{code}")
                        elif code in ANSI_STYLES:
                            tags.append(f"style_{code}")
                    current_tags = tuple(tags) if tags else ()
            else:
                if part:
                    tags = current_tags if current_tags else (msg_type,)
                    self.text.insert(tk.END, part, tags)
                    
        # Limit lines
        self._limit_lines()
        
        self.text.configure(state=tk.DISABLED)
        
        if self._auto_scroll.get():
            self.text.see(tk.END)
            
    def _limit_lines(self):
        """Limit total lines in console."""
        lines = int(self.text.index('end-1c').split('.')[0])
        if lines > self.max_lines:
            self.text.configure(state=tk.NORMAL)
            self.text.delete("1.0", f"{lines - self.max_lines}.0")
            self.text.configure(state=tk.DISABLED)
        
    def _filter(self, *args):
        self._filter_level = self.filter_var.get()
        self._search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        # Would need to re-render - for now just affects new output
        
    def _on_filter_change(self, value):
        self._filter_level = value
        # Would re-render filtered content
        
    def write_system(self, text: str):
        self.write(text, "system")

    def clear(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.configure(state=tk.DISABLED)
        
    def copy_all(self):
        self.clipboard_clear()
        self.clipboard_append(self.text.get("1.0", tk.END))
        
    def copy_selection(self):
        try:
            sel = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(sel)
        except tk.TclError:
            pass
            
    def pause(self):
        self._paused = True
        
    def resume(self):
        self._paused = False
        
    def flush(self):
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
    """File-like object to redirect stdout/stderr."""
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