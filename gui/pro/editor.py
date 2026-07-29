"""
ZapPhysics Professional — Code Editor
Syntax-highlighted code editor with line numbers, minimap, and advanced features.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, List, Dict, Tuple, Callable, Any
from pathlib import Path
import re
import threading
import queue
import time
import os


# ════════════════════════════════════════════════════════════════════
# Syntax Highlighting
# ════════════════════════════════════════════════════════════════════

class ZapSyntaxHighlighter:
    """Syntax highlighter for Zap language."""
    
    # Zap language keywords and patterns
    PATTERNS = [
        # Comments
        (r'#.*$', 'comment'),
        
        # Strings (double and single quoted, with escapes)
        (r'"(?:[^"\\]|\\.)*"', 'string'),
        (r"'(?:[^'\\]|\\.)*'", 'string'),
        
        # Numbers (int, float, scientific)
        (r'\b\d+\.\d+([eE][+-]?\d+)?\b', 'number'),
        (r'\b\d+[eE][+-]?\d+\b', 'number'),
        (r'\b\d+\.\d+\b', 'number'),
        (r'\b\d+\b', 'number'),
        
        # Keywords - Control flow
        (r'\b(if|el|for|while|ret|break|continue|match|case)\b', 'keyword_control'),
        
        # Keywords - Declarations
        (r'\b(let|fn|class|import|async|await)\b', 'keyword_decl'),
        
        # Types
        (r'\b(int|float|string|bool|none|list|dict|Vec2|Vec3|Vec4|AABB)\b', 'type'),
        
        # Built-in functions
        (r'\b(say|show|print|len|range|sin|cos|tan|sqrt|abs|floor|ceil|round|min|max|sum|random|now|wait|clear|int|float|str|bool|list|dict|map|filter|reduce|Vec2|Vec3|Vec4|AABB|Particle|World|Quadtree|UniformGrid)\b', 'builtin'),
        
        # Operators
        (r'[+\-*/%=<>!&|^~]+', 'operator'),
        
        # Brackets/punctuation
        (r'[\(\)\{\}\[\],;:.]+', 'bracket'),
        
        # Identifiers (must be last)
        (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'identifier'),
    ]
    
    TAG_STYLES = {
        'comment': '#6a9955',
        'string': '#ce9178',
        'number': '#b5cea8',
        'keyword_control': '#c586c0',
        'keyword_decl': '#569cd6',
        'type': '#4ec9b0',
        'builtin': '#dcdcaa',
        'operator': '#d4d4d4',
        'bracket': '#d4d4d4',
        'identifier': '#d4d4d4',
        'error': '#f85149',
    }
    
    def __init__(self, text_widget: tk.Text):
        self.text = text_widget
        self._setup_tags()
        self._compile_patterns()
        self._highlight_job = None
        self._pending = False
        
    def _setup_tags(self):
        for tag, color in self.TAG_STYLES.items():
            self.text.tag_configure(tag, foreground=color)
            
    def _compile_patterns(self):
        self.compiled_patterns = [
            (re.compile(pattern, re.MULTILINE), tag)
            for pattern, tag in self.PATTERNS
        ]
        
    def highlight(self, event=None):
        """Trigger syntax highlighting (debounced)."""
        if self._highlight_job:
            self.text.after_cancel(self._highlight_job)
        self._highlight_job = self.text.after(50, self._do_highlight)
        
    def _do_highlight(self):
        """Perform syntax highlighting on visible range."""
        self._highlight_visible_range()
        self._highlight_job = None
        
    def _highlight_visible_range(self):
        """Highlight only the visible portion of text."""
        # Get visible range
        first = self.text.index("@0,0")
        last = self.text.index(f"@0,{self.text.winfo_height()}")
        
        # Expand to full lines
        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 1
        
        start = f"{first_line}.0"
        end = f"{last_line}.0"
        
        # Remove existing tags in range
        for tag in self.TAG_STYLES.keys():
            self.text.tag_remove(tag, start, end)
            
        text_content = self.text.get(start, end)
        if not text_content.strip():
            return
            
        # Apply highlighting
        for pattern, tag in self.compiled_patterns:
            for match in pattern.finditer(text_content):
                start_pos = f"{start}+{match.start()}c"
                end_pos = f"{start}+{match.end()}c"
                self.text.tag_add(tag, start_pos, end_pos)
                
    def force_highlight(self):
        """Force full document highlight."""
        self._highlight_job = None
        self._do_highlight_full()
        
    def _do_highlight_full(self):
        """Highlight entire document."""
        # Remove all tags
        for tag in self.TAG_STYLES.keys():
            self.text.tag_remove(tag, "1.0", tk.END)
            
        content = self.text.get("1.0", "end-1c")
        if not content.strip():
            return
            
        for pattern, tag in self.compiled_patterns:
            for match in pattern.finditer(content):
                start_pos = f"1.0+{match.start()}c"
                end_pos = f"1.0+{match.end()}c"
                self.text.tag_add(tag, start_pos, end_pos)


class LineNumbers(ctk.CTkCanvas):
    """Line number gutter with current line highlighting."""
    
    def __init__(self, master, text_widget: tk.Text, **kwargs):
        super().__init__(
            master,
            width=50,
            bg="#161b22",
            highlightthickness=0,
            **kwargs
        )
        self.text_widget = text_widget
        self.font = ("JetBrains Mono", 11) if self._font_exists("JetBrains Mono") else ("Consolas", 11)
        self.line_height = 20
        self.current_line = 1
        
        # Bind events
        text_widget.bind("<KeyRelease>", self._on_change)
        text_widget.bind("<MouseWheel>", self._on_scroll)
        text_widget.bind("<ButtonRelease-1>", self._on_click)
        text_widget.bind("<Configure>", self._on_configure)
        text_widget.bind("<<Change>>", self._on_change)
        
    def _font_exists(self, name: str) -> bool:
        import tkinter.font as tkfont
        return name in tkfont.families()
        
    def _on_change(self, event=None):
        self.redraw()
        
    def _on_scroll(self, event):
        self.redraw()
        
    def _on_click(self, event):
        self.redraw()
        
    def _on_configure(self, event):
        self.redraw()
        
    def redraw(self):
        """Redraw line numbers."""
        self.delete("all")
        
        try:
            first = self.text_widget.index("@0,0")
            last = self.text_widget.index(f"@0,{self.winfo_height()}")
        except tk.TclError:
            return
            
        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 1
        
        # Get current line
        try:
            self.current_line = int(self.text_widget.index(tk.INSERT).split(".")[0])
        except:
            self.current_line = 1
            
        for i in range(first_line, last_line + 1):
            y = (i - first_line) * self.line_height + 2
            
            # Highlight current line
            if i == self.current_line:
                self.create_rectangle(
                    0, y - 2, 50, y + self.line_height - 2,
                    fill="#1e2a38", outline=""
                )
                fill = "#58a6ff"
                font = ("JetBrains Mono", 11, "bold") if self._font_exists("JetBrains Mono") else ("Consolas", 11, "bold")
            else:
                fill = "#8b949e"
                font = ("JetBrains Mono", 11) if self._font_exists("JetBrains Mono") else ("Consolas", 11)
                
            self.create_text(
                46, y,
                text=str(i),
                anchor="e",
                fill="#484f58" if i != self.current_line else "#58a6ff",
                font=font
            )


class MiniMap(ctk.CTkCanvas):
    """Code minimap with viewport indicator."""
    
    def __init__(self, master, text_widget: tk.Text, **kwargs):
        super().__init__(
            master,
            width=80,
            bg="#0d1117",
            highlightthickness=0,
            **kwargs
        )
        self.text_widget = text_widget
        self.scale = 0.2  # Scale factor
        self.viewport_rect = None
        self.char_width = 6
        self.char_height = 2
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        
        # Bind text events
        text_widget.bind("<KeyRelease>", self._on_change)
        text_widget.bind("<MouseWheel>", self._on_scroll)
        text_widget.bind("<ButtonRelease-1>", self._on_click)
        
    def _on_change(self, event=None):
        self.after(10, self.redraw)
        
    def _on_scroll(self, event):
        self.redraw()
        
    def _on_click(self, event):
        self._scroll_to(event.y)
        
    def _on_drag(self, event):
        self._scroll_to(event.y)
        
    def _scroll_to(self, y):
        """Scroll editor to position."""
        line = max(1, int(y / self.char_height))
        self.text_widget.yview_moveto(line / max(1, self.text_widget.count("1.0", "end", "displaylines")[0]))
        
    def redraw(self):
        """Redraw minimap."""
        self.delete("all")
        
        try:
            # Get text content
            content = self.text_widget.get("1.0", "end-1c")
            lines = content.split('\n')
            
            # Draw lines as small blocks
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                y = i * self.char_height
                # Color based on content
                color = "#30363d"
                if line.strip().startswith('#'):
                    color = "#6a9955"
                elif any(kw in line for kw in ['fn ', 'class ', 'let ', 'if ', 'for ', 'while ']):
                    color = "#c586c0"
                elif '"' in line or "'" in line:
                    color = "#ce9178"
                    
                self.create_rectangle(
                    4, i * self.char_height + 2,
                    78, (i + 1) * self.char_height,
                    fill=color, outline=""
                )
                
            # Draw viewport indicator
            try:
                first = self.text_widget.index("@0,0")
                last = self.text_widget.index(f"@0,{self.text_widget.winfo_height()}")
                first_line = int(first.split(".")[0])
                last_line = int(last.split(".")[0])
                
                y1 = first_line * self.char_height
                y2 = last_line * self.char_height
                
                if self.viewport_rect:
                    self.delete(self.viewport_rect)
                self.viewport_rect = self.create_rectangle(
                    2, y1, 78, y2,
                    outline="#58a6ff", width=2
                )
            except:
                pass
                
        except Exception:
            pass
            
    def _on_change(self, event=None):
        self.after(50, self.redraw)
        
    def _on_scroll(self, event):
        self.redraw()


# ════════════════════════════════════════════════════════════════════
# Main Editor Widget
# ════════════════════════════════════════════════════════════════════

class CodeEditor(ctk.CTkFrame):
    """Professional code editor with all modern features."""
    
    def __init__(
        self,
        master,
        on_save: Optional[Callable] = None,
        on_run: Optional[Callable] = None,
        on_content_changed: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.on_save = on_save
        self.on_run = on_run
        self.on_content_changed = on_content_changed
        
        self.current_file: Optional[Path] = None
        self.modified = False
        self._highlight_job = None
        
        self._build_ui()
        self._bind_events()
        
    def _build_ui(self):
        """Build the editor UI."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent", height=40)
        toolbar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=8, pady=(8, 0))
        toolbar.grid_columnconfigure(2, weight=1)
        
        # File info
        self.file_label = ctk.CTkLabel(
            toolbar,
            text="Untitled.zpx",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#e6edf3"
        )
        self.file_label.pack(side="left", padx=12, pady=4)
        
        # Modified indicator
        self.modified_indicator = ctk.CTkLabel(
            toolbar,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#f85149"
        )
        self.modified_indicator.pack(side="left", padx=4)
        
        # Spacer
        ctk.CTkFrame(toolbar, fg_color="transparent").pack(side="left", expand=True, fill="x")
        
        # Toolbar buttons
        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(side="right", padx=8)
        
        from .widgets import ProButton
        
        ProButton(btn_frame, text="▶ Run", variant="primary", width=90, command=self._on_run).pack(side="left", padx=4)
        ProButton(btn_frame, text="Save", variant="secondary", width=80, command=self.save_file).pack(side="left", padx=4)
        
        # Main editor area
        editor_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=8, border_width=1, border_color="#30363d")
        editor_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=8, pady=8)
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(1, weight=1)
        
        # Text editor
        self.text = tk.Text(
            editor_frame,
            bg="#0d1117",
            fg="#e6edf3",
            insertbackground="#58a6ff",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            font=("JetBrains Mono", 12) if self._font_exists("JetBrains Mono") else ("Consolas", 12),
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=10,
            tabs=("4c",),
        )
        self.text.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        
        # Line numbers
        self.line_numbers = LineNumbers(editor_frame, self.text)
        self.line_numbers.grid(row=0, column=0, sticky="ns", padx=(2, 0), pady=2)
        
        # Scrollbars
        v_scroll = ctk.CTkScrollbar(editor_frame, command=self._on_vscroll)
        v_scroll.grid(row=0, column=2, sticky="ns", pady=2)
        h_scroll = ctk.CTkScrollbar(editor_frame, orientation="horizontal", command=self.text.xview)
        h_scroll.grid(row=1, column=1, sticky="ew", padx=2)
        
        self.text.configure(yscrollcommand=self._on_yscroll, xscrollcommand=h_scroll.set)
        
        # Minimap
        self.minimap = MiniMap(editor_frame, self.text)
        self.minimap.grid(row=0, column=3, sticky="ns", padx=(0, 2), pady=2)
        
        # Status bar
        status_frame = ctk.CTkFrame(self, fg_color="#161b22", height=28, corner_radius=0, border_width=1, border_color="#30363d")
        status_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 8))
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.status_pos = ctk.CTkLabel(
            self, text="Ln 1, Col 1", font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#8b949e", anchor="w"
        )
        self.status_pos.grid(row=2, column=0, sticky="w", padx=16, pady=2)
        
        self.status_encoding = ctk.CTkLabel(
            self, text="UTF-8", font=ctk.CTkFont(size=11),
            text_color="#8b949e"
        )
        self.status_encoding.grid(row=2, column=1, sticky="e", padx=16, pady=2)
        
        self.status_eol = ctk.CTkLabel(
            self, text="LF", font=ctk.CTkFont(size=11),
            text_color="#8b949e"
        )
        self.status_eol.grid(row=2, column=2, sticky="e", padx=16, pady=2)
        
        # Syntax highlighter
        self.highlighter = ZapSyntaxHighlighter(self.text)
        
    def _font_exists(self, name: str) -> bool:
        import tkinter.font as tkfont
        return name in tkfont.families()
        
    def _bind_events(self):
        """Bind editor events."""
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<ButtonRelease-1>", self._on_click)
        self.text.bind("<MouseWheel>", self._on_mousewheel)
        self.text.bind("<Control-s>", lambda e: self.save())
        self.text.bind("<Control-Shift-S>", lambda e: self.save_as())
        self.text.bind("<Control-o>", lambda e: self.open_file())
        self.text.bind("<Control-n>", lambda e: self.new_file())
        self.text.bind("<F5>", lambda e: self._on_run())
        self.text.bind("<Tab>", self._on_tab)
        self.text.bind("<Shift-Tab>", lambda e: self._on_shift_tab())
        self.text.bind("<Return>", self._on_return)
        self.text.bind("<<Change>>", self._on_content_change)
        
    def _on_key_release(self, event):
        self.modified = True
        self._update_modified_indicator()
        self._update_status()
        self.highlighter.highlight()
        
        if self.on_content_changed:
            self.on_content_changed(self.get_code())
            
    def _on_click(self, event):
        self._update_status()
        self.minimap.redraw()
        
    def _on_mousewheel(self, event):
        self.minimap.redraw()
        
    def _on_return(self, event):
        # Auto-indent
        current_line = self.text.index(tk.INSERT).split(".")[0]
        line_text = self.text.get(f"{current_line}.0", f"{current_line}.end")
        indent = len(line_text) - len(line_text.lstrip())
        if indent > 0:
            self.text.insert(tk.INSERT, "\n" + " " * indent)
            return "break"
            
    def _on_tab(self, event):
        self.text.insert(tk.INSERT, "    ")
        return "break"
        
    def _on_shift_tab(self, event):
        current = self.text.index(tk.INSERT)
        line_start = f"{current.split('.')[0]}.0"
        line_text = self.text.get(line_start, f"{line_start} lineend")
        if line_text.startswith("    "):
            self.text.delete(line_start, f"{line_start}+4c")
        return "break"
        
    def _on_content_change(self, event=None):
        self.modified = True
        self._update_modified_indicator()
        
    def _on_vscroll(self, *args):
        self.text.yview(*args)
        self.minimap.redraw()
        
    def _on_yscroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        if len(args) > 1 and args[0] == "scroll":
            self.minimap.redraw()
            
    def _on_run(self):
        if self.on_run:
            self.on_run()
            
    def _update_modified_indicator(self):
        if self.modified:
            self.modified_indicator.configure(text="●")
            self.file_label.configure(text=f"{self.current_file.name if self.current_file else 'Untitled.zpx'} *")
        else:
            self.modified_indicator.configure(text="")
            self.file_label.configure(text=self.current_file.name if self.current_file else "Untitled.zpx")
            
    def _update_status(self):
        pos = self.text.index(tk.INSERT)
        line, col = pos.split(".")
        self.status_pos.configure(text=f"Ln {line}, Col {int(col)+1}")

    # ═══════════════════════════════════════════════════════════════════
    # File Operations
    # ═══════════════════════════════════════════════════════════════════

    def new_file(self):
        if self.modified and not self._confirm_discard():
            return
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.modified = False
        self._update_modified_indicator()
        self._update_status()
        self.highlighter.force_highlight()
        
    def open_file(self, path: Optional[Path] = None) -> bool:
        if path is None:
            path = filedialog.askopenfilename(
                defaultextension=".zpx",
                filetypes=[("ZPX files", "*.zpx"), ("All files", "*.*")],
                initialdir=str(Path.cwd() / "examples")
            )
        if not path:
            return False
            
        if self.modified and not self._confirm_discard():
            return False
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.current_file = Path(path)
            self.modified = False
            self._update_modified_indicator()
            self._update_status()
            self.highlighter.force_highlight()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")
            return False
            
    def save_file(self) -> bool:
        if self.current_file:
            return self._write_file(self.current_file)
        else:
            return self.save_as()
            
    def save_as(self) -> bool:
        path = filedialog.asksaveasfilename(
            defaultextension=".zpx",
            filetypes=[("ZPX files", "*.zpx"), ("All files", "*.*")],
            initialdir=str(Path.cwd() / "examples")
        )
        if path:
            return self._write_file(Path(path))
        return False
        
    def _write_file(self, path: Path) -> bool:
        try:
            content = self.text.get("1.0", "end-1c")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.current_file = path
            self.modified = False
            self._update_modified_indicator()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
            return False
            
    def _confirm_discard(self) -> bool:
        return messagebox.askyesno(
            "Unsaved Changes",
            "You have unsaved changes. Discard them?",
            icon="warning"
        )
        
    # ═══════════════════════════════════════════════════════════════════
    # Public API
    # ═══════════════════════════════════════════════════════════════════
    
    def get_code(self) -> str:
        return self.text.get("1.0", "end-1c")
        
    def set_code(self, code: str):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)
        self.highlighter.force_highlight()
        
    def get_selection(self) -> str:
        try:
            return self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return ""
            
    def set_selection(self, text: str):
        try:
            self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text.insert(tk.INSERT, text)
        except tk.TclError:
            pass
            
    def load_file(self, path: str) -> bool:
        return self.open_file(path)

    def clear(self):
        self.text.delete("1.0", tk.END)
        self.modified = False
        self._update_modified_indicator()
        
    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass
            
    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass
            
    def find(self, text: str, forward: bool = True) -> bool:
        """Find text in editor."""
        start = "insert" if forward else "insert-1c"
        pos = self.text.search(text, start, stopindex="end", forwards=forward)
        if pos:
            end = f"{pos}+{len(text)}c"
            self.text.tag_remove(tk.SEL, "1.0", tk.END)
            self.text.tag_add(tk.SEL, pos, end)
            self.text.mark_set(tk.INSERT, pos)
            self.text.see(pos)
            return True
        return False
        
    def replace(self, find_text: str, replace_text: str, all_occurrences: bool = False) -> int:
        count = 0
        content = self.get_code()
        if all_occurrences:
            new_content = content.replace(find_text, replace_text)
            count = content.count(find_text)
            self.set_code(new_content)
        else:
            pos = self.text.search(find_text, "insert", stopindex="end")
            if pos:
                end = f"{pos}+{len(find_text)}c"
                self.text.delete(pos, end)
                self.text.insert(pos, replace_text)
                count = 1
        return count
        
    def goto_line(self, line: int):
        self.text.mark_set(tk.INSERT, f"{line}.0")
        self.text.see(f"{line}.0")
        self._update_status()
        
    def comment_selection(self):
        try:
            sel_start = self.text.index(tk.SEL_FIRST)
            sel_end = self.text.index(tk.SEL_LAST)
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])
            
            for line in range(start_line, end_line + 1):
                line_start = f"{line}.0"
                line_text = self.text.get(line_start, f"{line_start} lineend")
                if not line_text.lstrip().startswith("#"):
                    self.text.insert(line_start, "# ")
        except tk.TclError:
            pass
            
    def uncomment_selection(self):
        try:
            sel_start = self.text.index(tk.SEL_FIRST)
            sel_end = self.text.index(tk.SEL_LAST)
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])
            
            for line in range(start_line, end_line + 1):
                line_start = f"{line}.0"
                line_text = self.text.get(line_start, f"{line_start} lineend")
                if line_text.startswith("# "):
                    self.text.delete(line_start, f"{line_start}+2c")
                elif line_text.startswith("#"):
                    self.text.delete(line_start, f"{line_start}+1c")
        except tk.TclError:
            pass
            
    def format_document(self):
        """Basic code formatting (placeholder for future LSP integration)."""
        # This would integrate with a formatter like black or a custom Zap formatter
        pass