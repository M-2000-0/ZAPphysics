"""Script Editor with Zap syntax highlighting."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from gui.theme import *


class LineNumbers(tk.Canvas):
    """Line number gutter for the text editor."""
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_widget = text_widget
        self.config(width=50, bg=LINE_NUMBER, highlightthickness=0)
        self.font = ("Consolas", 10)

    def redraw(self):
        """Redraw line numbers."""
        self.delete("all")
        first_line = int(self.text_widget.index("@0,0").split(".")[0])
        last_line = int(self.text_widget.index(f"@0,{self.winfo_height()}").split(".")[0])
        line_height = 20  # Approximate

        for i in range(first_line, last_line + 1):
            y = (i - first_line) * line_height + 2
            self.create_text(45, y, text=str(i), anchor="e", fill=FG_DIM, font=self.font)


class ScriptEditor(ttk.Frame):
    """Code editor with Zap syntax highlighting."""
    
    ZAP_KEYWORDS = {
        'control': ['if', 'el', 'for', 'while', 'ret', 'break', 'continue', 'match', 'case'],
        'declaration': ['let', 'fn', 'class', 'import', 'async', 'await'],
        'types': ['int', 'float', 'string', 'bool', 'none', 'list', 'dict', 'Vec2', 'Vec3', 'Vec4', 'AABB'],
        'builtins': ['say', 'show', 'print', 'len', 'range', 'sin', 'cos', 'tan', 'sqrt', 'abs', 
                     'floor', 'ceil', 'round', 'min', 'max', 'sum', 'random', 'now', 'wait', 'clear',
                     'int', 'float', 'str', 'bool', 'list', 'dict', 'map', 'filter', 'reduce',
                     'Vec2', 'Vec3', 'Vec4', 'AABB', 'Particle', 'World', 'Quadtree', 'UniformGrid'],
        'operators': ['and', 'or', 'not', 'in', 'is', 'as'],
    }

    def __init__(self, parent, zap_runner):
        super().__init__(parent)
        self.zap_runner = zap_runner
        self.current_file = None
        self.modified = False
        self._build_ui()
        self._setup_syntax_highlighting()
        self._bind_events()

    def _build_ui(self):
        """Build the editor UI with line numbers."""
        # Create paned window for line numbers + editor
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, 
                                     bg=BG, sashwidth=0, showhandle=False)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Line numbers canvas
        self.line_numbers = LineNumbers(self.paned, None, bg=LINE_NUMBER)
        self.paned.add(self.line_numbers, width=50)

        # Text editor with scrollbar
        editor_frame = ttk.Frame(self.paned)
        self.paned.add(editor_frame)

        self.text = tk.Text(
            editor_frame,
            bg=PANEL,
            fg=FG,
            insertbackground=ACCENT,
            selectbackground=SELECTION,
            selectforeground=FG,
            font=("Consolas", 10),
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            borderwidth=0,
            highlightthickness=0,
            tabs=("4c",)
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scroll = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self._on_scroll)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll = ttk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=self.text.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Set line_numbers reference
        self.line_numbers.text_widget = self.text

        # Status bar
        self.status_var = tk.StringVar(value="Ln 1, Col 1  |  Zap  |  UTF-8")
        status = ttk.Label(self, textvariable=self.status_var, anchor=tk.W, 
                          background=PANEL_LIGHT, foreground=FG_DIM, font=("Consolas", 8))
        status.pack(fill=tk.X, side=tk.BOTTOM, padx=2, pady=(2, 0))

    def _setup_syntax_highlighting(self):
        """Configure syntax highlighting tags."""
        # Define colors
        colors = {
            'control': ACCENT,
            'declaration': "#c586c0",
            'types': "#4ec9b0",
            'builtins': "#dcdcaa",
            'operators': "#d4d4d4",
            'string': "#ce9178",
            'comment': "#6a9955",
            'number': "#b5cea8",
            'operator': "#d4d4d4",
            'bracket': "#d4d4d4",
        }

        for tag, color in colors.items():
            self.text.tag_configure(tag, foreground=color)

        # Special tags
        self.text.tag_configure('error', foreground=ERROR, underline=True)
        self.text.tag_configure('current_line', background="#2a2d2e")
        self.text.tag_configure('selection', background=SELECTION)

        # Compile regex patterns
        self.patterns = []
        
        # Comments
        self.patterns.append((r'#.*$', 'comment'))
        
        # Strings (single and double quoted, with escaped quotes)
        self.patterns.append((r'"(?:[^"\\]|\\.)*"', 'string'))
        self.patterns.append((r"'(?:[^'\\]|\\.)*'", 'string'))
        
        # Numbers (int, float, scientific)
        self.patterns.append((r'\b\d+\.\d+([eE][+-]?\d+)?\b', 'number'))
        self.patterns.append((r'\b\d+[eE][+-]?\d+\b', 'number'))
        self.patterns.append((r'\b\d+\.\d+\b', 'number'))
        self.patterns.append((r'\b\d+\b', 'number'))
        
        # Keywords
        for category, words in self.ZAP_KEYWORDS.items():
            pattern = r'\b(' + '|'.join(re.escape(w) for w in words) + r')\b'
            self.patterns.append((pattern, category))
        
        # Operators and punctuation
        self.patterns.append((r'[+\-*/%=<>!&|^~]+', 'operator'))
        self.patterns.append((r'[\(\)\{\}\[\],;:.]+', 'bracket'))

    def _bind_events(self):
        """Bind editor events."""
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<ButtonRelease-1>", self._update_status)
        self.text.bind("<KeyRelease>", self._update_status, add="+")
        self.text.bind("<MouseWheel>", self._on_scroll)
        self.text.bind("<Control-Key-a>", self._select_all)
        self.text.bind("<Control-Key-s>", lambda e: self.save_file())
        self.text.bind("<Control-Key-o>", lambda e: self.master.master._open_script() if hasattr(self.master, 'master') else None)
        
        # Tab key handling
        self.text.bind("<Tab>", self._on_tab)
        self.text.bind("<Shift-Tab>", self._on_shift_tab)

        # Auto-indent on newline
        self.text.bind("<Return>", self._on_return)

    def _on_key_release(self, event=None):
        """Trigger syntax highlighting on key release."""
        self._highlight_syntax()
        self.modified = True
        self._update_status()

    def _update_status(self, event=None):
        """Update status bar with line/column info."""
        pos = self.text.index(tk.INSERT)
        line, col = pos.split(".")
        self.status_var.set(f"Ln {line}, Col {int(col)+1}  |  Zap  |  UTF-8")
        self.line_numbers.redraw()

    def _on_scroll(self, *args):
        """Handle scrolling - sync line numbers."""
        if len(args) == 2 and args[0] == 'moveto':
            self.text.yview(*args)
        elif len(args) == 2 and args[0] == 'scroll':
            self.text.yview(*args)
        self.line_numbers.redraw()
        return "break"

    def _on_tab(self, event):
        """Handle Tab key - insert 4 spaces."""
        self.text.insert(tk.INSERT, "    ")
        return "break"

    def _on_shift_tab(self, event):
        """Handle Shift+Tab - dedent."""
        current_line = self.text.index("insert linestart")
        line_text = self.text.get(current_line, f"{current_line} lineend")
        if line_text.startswith("    "):
            self.text.delete(current_line, f"{current_line}+4c")
        return "break"

    def _on_return(self, event):
        """Auto-indent on new line."""
        current_line = self.text.index("insert linestart")
        line_text = self.text.get(current_line, f"{current_line} lineend")
        indent = len(line_text) - len(line_text.lstrip())
        self.text.insert(tk.INSERT, "\n" + " " * indent)
        return "break"

    def _select_all(self, event):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return "break"

    def _highlight_syntax(self):
        """Apply syntax highlighting to visible text."""
        # Remove existing tags
        for tag in ['control', 'declaration', 'types', 'builtins', 'operators', 
                    'string', 'comment', 'number', 'operator', 'bracket']:
            self.text.tag_remove(tag, "1.0", tk.END)

        # Get visible range
        first = self.text.index("@0,0")
        last = self.text.index(f"@0,{self.text.winfo_height()}")
        
        # Expand to full lines
        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 1
        start = f"{first_line}.0"
        end = f"{last_line}.0"

        text_content = self.text.get(start, end)
        if not text_content.strip():
            return

        # Apply patterns
        for pattern, tag in self.patterns:
            for match in re.finditer(pattern, text_content, re.MULTILINE):
                start_pos = f"{start}+{match.start()}c"
                end_pos = f"{start}+{match.end()}c"
                self.text.tag_add(tag, start_pos, end_pos)

    def new_file(self):
        """Create new empty file."""
        if self.modified and not self._confirm_discard():
            return
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.modified = False
        self._update_title()

    def load_file(self, path: str):
        """Load file from path."""
        if self.modified and not self._confirm_discard():
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.current_file = path
            self.modified = False
            self._update_title()
            self._highlight_syntax()
            self._update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def save_file(self):
        """Save to current file."""
        if self.current_file:
            self._write_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save to new file."""
        path = filedialog.asksaveasfilename(
            defaultextension=".zap",
            filetypes=[("Zap files", "*.zap"), ("All files", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "..", "..", "examples")
        )
        if path:
            self._write_file(path)

    def _write_file(self, path: str):
        try:
            content = self.text.get("1.0", "end-1c")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.current_file = path
            self.modified = False
            self._update_title()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def _confirm_discard(self) -> bool:
        """Ask user to save changes."""
        result = messagebox.askyesnocancel("Unsaved Changes", 
            "You have unsaved changes. Save before continuing?")
        if result is None:
            return False
        if result:
            self.save_file()
            return not self.modified
        return True

    def _update_title(self):
        """Update window title with file name."""
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        if self.modified:
            name += " *"
        # Update parent window title
        if hasattr(self.master, 'master') and hasattr(self.master.master, 'title'):
            self.master.master.title(f"ZapPhysics v4.0 — {name}")

    def get_code(self) -> str:
        """Get current editor code."""
        return self.text.get("1.0", "end-1c")

    def get_selection(self) -> str:
        """Get selected text."""
        try:
            return self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return ""

    def set_code(self, code: str):
        """Set editor code."""
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)
        self._highlight_syntax()
        self._update_status()