"""
ZapPhysics Modern Desktop GUI — Built with CustomTkinter
Modern dark-theme IDE with rounded widgets, smooth animations, and contemporary UX.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import threading
import queue
import subprocess
import webbrowser
from pathlib import Path
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

# ─── Paths ───
ROOT = Path(__file__).parent.parent
ZAP_SRC = ROOT / "zap" / "src"
EXAMPLES_DIR = ROOT / "examples"
sys.path.insert(0, str(ZAP_SRC))

# ─── Theme ───
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Custom color palette
COLORS = {
    "bg": "#0d1117",           # GitHub dark background
    "panel": "#161b22",        # Panel background
    "panel_hover": "#1f2428",  # Hover state
    "border": "#30363d",       # Borders
    "accent": "#58a6ff",       # Primary blue
    "accent_hover": "#79b8ff",
    "accent_dim": "#1f6feb",   # Pressed
    "success": "#3fb950",
    "warning": "#d29922",
    "error": "#f85149",
    "fg": "#e6edf3",           # Primary text
    "fg_secondary": "#8b949e", # Secondary text
    "fg_muted": "#6e7681",     # Muted text
    "code_bg": "#0d1117",      # Editor background
    "line_num": "#1f2428",     # Line numbers
    "selection": "#264f78",    # Selection
}

# ─── Demo Catalog ───
DEMOS = {
    "orbital": ("Orbital Mechanics", "examples/demo_orbital.zap", "N-body gravity, Hohmann transfers"),
    "orbital3d": ("3D Orbital (VV)", "examples/demo_orbital3d.zap", "3D velocity verlet integration"),
    "lambert": ("Lambert Solver", "examples/demo_lambert.zap", "Orbital targeting & rendezvous"),
    "porkchop": ("Porkchop Plot", "examples/demo_porkchop.zap", "Earth→Mars launch windows"),
    "rocket": ("Rocket Engineering", "examples/demo_rocket.zap", "Multi-stage design & trajectory"),
    "flight": ("Flight Dynamics", "examples/demo_flight.zap", "Aircraft aerodynamics & envelope"),
    "structural": ("Structural Eng", "examples/demo_structural.zap", "Truss & beam analysis"),
    "game": ("Game Physics", "examples/demo_game.zap", "Platformer, top-down, ragdoll"),
    "collisions": ("Collisions", "examples/collisions.zap", "Elastic collision dynamics"),
    "springs": ("Spring-Mass", "examples/springs.zap", "Oscillator systems"),
    "chemistry": ("Chemistry Lab", "examples/chemistry.zap", "Molecules, reactions, thermo"),
    "elements": ("Periodic Table", "examples/demo_elements.zap", "118 elements"),
    "kinetics": ("Reaction Kinetics", "examples/demo_kinetics.zap", "Rate laws, equilibrium, enzymes"),
    "em": ("Electromagnetics", "examples/demo_em.zap", "Coulomb, Lorentz, fields"),
    "fluid": ("SPH Fluids", "examples/demo_fluid.zap", "Smoothed particle hydrodynamics"),
    "rigid": ("Rigid Body", "examples/demo_rigid.zap", "Rotation, torque, inertia"),
    "tensor": ("Tensor N-Body", "examples/tensor.zap", "Matrix force calculations"),
    "visual": ("ASCII Viz", "examples/demo_visual.zap", "Charts, sparklines, heatmaps"),
    "art": ("Generative Art", "examples/demo_art.zap", "Particle fountains, spirals"),
    "broadphase": ("Broadphase", "examples/demo_broadphase.zap", "Grid & quadtree collision"),
    "constraints": ("Constraints", "examples/demo_constraints.zap", "Distance, spring, hinge, slider"),
}


# ════════════════════════════════════════════════════════════════════
# Modern Widgets
# ════════════════════════════════════════════════════════════════════

class ModernFrame(ctk.CTkFrame):
    """Frame with subtle border and hover effect."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["panel"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=10,
            **kwargs
        )


class ModernButton(ctk.CTkButton):
    """Modern button with consistent styling."""
    def __init__(self, master, variant="primary", **kwargs):
        variants = {
            "primary": {"fg_color": COLORS["accent"], "hover_color": COLORS["accent_hover"], "text_color": "#fff"},
            "secondary": {"fg_color": COLORS["panel_hover"], "hover_color": COLORS["border"], "text_color": COLORS["fg"], "border_width": 1, "border_color": COLORS["border"]},
            "danger": {"fg_color": COLORS["error"], "hover_color": "#f85149", "text_color": "#fff"},
            "ghost": {"fg_color": "transparent", "hover_color": COLORS["panel_hover"], "text_color": COLORS["fg_secondary"], "border_width": 0},
        }
        style = variants.get(variant, variants["primary"])
        # Allow height to be overridden via kwargs
        height = kwargs.pop("height", 36)
        super().__init__(
            master,
            fg_color=style["fg_color"],
            hover_color=style["hover_color"],
            text_color=style.get("text_color", "#fff"),
            border_width=style.get("border_width", 0),
            border_color=style.get("border_color"),
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal"),
            height=height,
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["code_bg"],
            border_color=COLORS["border"],
            text_color=COLORS["fg"],
            placeholder_text_color=COLORS["fg_muted"],
            corner_radius=8,
            height=36,
            font=ctk.CTkFont(family="Consolas", size=12),
            **kwargs
        )


class ModernComboBox(ctk.CTkComboBox):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["panel"],
            border_color=COLORS["border"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["panel"],
            dropdown_hover_color=COLORS["panel_hover"],
            dropdown_text_color=COLORS["fg"],
            text_color=COLORS["fg"],
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            dropdown_font=ctk.CTkFont(family="Segoe UI", size=12),
            **kwargs
        )


class ModernSlider(ctk.CTkSlider):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            progress_color=COLORS["accent"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            corner_radius=8,
            **kwargs
        )


class ModernSwitch(ctk.CTkSwitch):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            progress_color=COLORS["accent"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            fg_color=COLORS["border"],
            **kwargs
        )


class ModernScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["fg_muted"],
            corner_radius=0,
            **kwargs
        )


class ModernTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["panel"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=10,
            segmented_button_fg_color=COLORS["panel_hover"],
            segmented_button_selected_color=COLORS["accent"],
            segmented_button_selected_hover_color=COLORS["accent_hover"],
            segmented_button_unselected_color=COLORS["panel_hover"],
            segmented_button_unselected_hover_color=COLORS["border"],
            text_color=COLORS["fg"],
            **kwargs
        )


# ════════════════════════════════════════════════════════════════════
# Code Editor with Syntax Highlighting
# ════════════════════════════════════════════════════════════════════

class CodeEditor(ctk.CTkFrame):
    """Modern code editor with line numbers and syntax highlighting."""
    
    ZAP_KEYWORDS = {
        "control": ["if", "el", "for", "while", "ret", "break", "continue", "match", "case"],
        "declare": ["let", "fn", "class", "import", "async", "await"],
        "types": ["int", "float", "string", "bool", "none", "list", "dict", "Vec2", "Vec3", "Vec4", "AABB"],
        "builtins": ["say", "show", "print", "len", "range", "sin", "cos", "tan", "sqrt", "abs",
                     "floor", "ceil", "round", "min", "max", "sum", "random", "now", "wait", "clear",
                     "Vec2", "Vec3", "Vec4", "AABB", "Particle", "World", "Quadtree", "UniformGrid"],
        "operators": ["and", "or", "not", "in", "is", "as"],
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent")
        
        self.current_file = None
        self.modified = False
        self._build_ui()
        self._setup_tags()
        self._bind_events()
        
    def _build_ui(self):
        # Main container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Line numbers canvas
        self.line_canvas = tk.Canvas(
            self,
            width=50,
            bg=COLORS["line_num"],
            highlightthickness=0,
            bd=0
        )
        self.line_canvas.grid(row=0, column=0, sticky="ns", padx=(0, 2))
        
        # Text widget
        self.text = tk.Text(
            self,
            bg=COLORS["code_bg"],
            fg=COLORS["fg"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["selection"],
            selectforeground=COLORS["fg"],
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
        self.text.grid(row=0, column=1, sticky="nsew")
        
        # Scrollbars
        v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=self._on_vscroll)
        v_scroll.grid(row=0, column=2, sticky="ns", padx=(0, 4))
        h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self.text.xview)
        h_scroll.grid(row=1, column=1, sticky="ew", padx=(4, 0))
        
        self.text.configure(yscrollcommand=self._on_yscroll, xscrollcommand=h_scroll.set)
        
        # Status bar
        self.status_var = ctk.StringVar(value="Ln 1, Col 1  •  Zap  •  UTF-8")
        status = ctk.CTkLabel(self, textvariable=self.status_var, 
                             font=ctk.CTkFont(size=11), text_color=COLORS["fg_muted"], anchor="w")
        status.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(4, 0))
        
    def _font_exists(self, name):
        import tkinter.font as tkfont
        return name in tkfont.families()

    def _setup_tags(self):
        # Syntax colors
        colors = {
            "control": "#c586c0",
            "declare": "#569cd6",
            "types": "#4ec9b0",
            "builtins": "#dcdcaa",
            "operators": "#d4d4d4",
            "string": "#ce9178",
            "comment": "#6a9955",
            "number": "#b5cea8",
            "operator": "#d4d4d4",
            "bracket": "#d4d4d4",
        }
        for tag, color in colors.items():
            self.text.tag_configure(tag, foreground=color)
        
        self.text.tag_configure("current_line", background="#1e2a38")
        self.text.tag_configure("error", underline=True, underlinefg="#f85149")

    def _bind_events(self):
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<ButtonRelease-1>", self._update_status)
        self.text.bind("<MouseWheel>", self._on_mousewheel)
        self.text.bind("<Control-a>", self._select_all)
        self.text.bind("<Control-s>", lambda e: self._trigger_save())
        self.text.bind("<Tab>", self._on_tab)
        self.text.bind("<Shift-Tab>", self._on_shift_tab)
        self.text.bind("<Return>", self._on_return)
        self.text.bind("<KeyRelease>", self._highlight, add="+")
        self.text.bind("<ButtonRelease-1>", self._highlight_line, add="+")

    def _on_vscroll(self, *args):
        self.text.yview(*args)
        self._redraw_lines()

    def _on_yscroll(self, *args):
        self.line_canvas.yview_moveto(args[0])
        if hasattr(self, '_scroll_job'):
            self.after_cancel(self._scroll_job)
        self._scroll_job = self.after(50, self._redraw_lines)

    def _on_mousewheel(self, event):
        self.text.yview_scroll(int(-event.delta/120), "units")
        self._redraw_lines()
        return "break"

    def _on_key_release(self, event):
        self.modified = True
        self._update_status()
        self._highlight_line()

    def _update_status(self, event=None):
        pos = self.text.index(tk.INSERT)
        line, col = pos.split(".")
        self.status_var.set(f"Ln {line}, Col {int(col)+1}  •  Zap  •  UTF-8")

    def _highlight_line(self, event=None):
        self.text.tag_remove("current_line", "1.0", tk.END)
        line = self.text.index(tk.INSERT).split(".")[0]
        self.text.tag_add("current_line", f"{line}.0", f"{line}.end")

    def _redraw_lines(self):
        self.line_canvas.delete("all")
        first = self.text.index("@0,0")
        last = self.text.index(f"@0,{self.line_canvas.winfo_height()}")
        first_line = int(first.split(".")[0])
        last_line = int(last.split(".")[0]) + 1
        
        line_height = 22
        for i in range(first_line, last_line + 1):
            y = (i - int(self.text.index("@0,0").split(".")[0])) * line_height + 2
            self.line_canvas.create_text(46, y, text=str(i), anchor="e", 
                                        fill=COLORS["fg_muted"], font=("JetBrains Mono", 11))

    def _highlight(self, event=None):
        """Syntax highlighting for visible lines."""
        first = self.text.index("@0,0")
        last = self.text.index(f"@0,{self.winfo_height()}")
        start_line = int(first.split(".")[0])
        end_line = int(last.split(".")[0]) + 1
        
        start = f"{start_line}.0"
        end = f"{end_line}.0"
        content = self.text.get(start, end)
        
        # Remove existing tags in range
        for tag in ["control", "declare", "types", "builtins", "operators", "string", "comment", "number", "operator", "bracket"]:
            self.text.tag_remove(tag, start, end)
        
        import re
        patterns = [
            (r'#.*$', 'comment'),
            (r'"(?:[^"\\]|\\.)*"', 'string'),
            (r"'(?:[^'\\]|\\.)*'", 'string'),
            (r'\b\d+\.\d+([eE][+-]?\d+)?\b', 'number'),
            (r'\b\d+[eE][+-]?\d+\b', 'number'),
            (r'\b\d+\.\d+\b', 'number'),
            (r'\b\d+\b', 'number'),
        ]
        for cat, words in self.ZAP_KEYWORDS.items():
            patterns.append((r'\b(' + '|'.join(re.escape(w) for w in words) + r')\b', cat))
        patterns.extend([
            (r'[+\-*/%=<>!&|^~]+', 'operator'),
            (r'[\(\)\{\}\[\],;:.]+', 'bracket'),
        ])
        
        for pattern, tag in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                s = f"{start}+{match.start()}c"
                e = f"{start}+{match.end()}c"
                self.text.tag_add(tag, s, e)

    def _highlight_line(self, event=None):
        # Throttle full highlight
        self.after(10, self._highlight)

    def _on_tab(self, event):
        self.text.insert(tk.INSERT, "    ")
        return "break"

    def _on_shift_tab(self, event):
        pos = self.text.index(tk.INSERT)
        line_start = f"{pos.split('.')[0]}.0"
        line_text = self.text.get(line_start, f"{line_start} lineend")
        if line_text.startswith("    "):
            self.text.delete(line_start, f"{line_start}+4c")
        return "break"

    def _on_return(self, event):
        current_line = self.text.index(tk.INSERT).split(".")[0]
        line_text = self.text.get(f"{current_line}.0", f"{current_line}.end")
        indent = len(line_text) - len(line_text.lstrip())
        self.text.insert(tk.INSERT, "\n" + " " * indent)
        return "break"

    def _select_all(self, event):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return "break"

    def _trigger_save(self):
        if hasattr(self, 'on_save'):
            self.on_save()

    # ─── File Operations ───
    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.current_file = path
            self.modified = False
            self._highlight()
            self._redraw_lines()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")
            return False

    def save_file(self, path=None):
        if path is None:
            path = self.current_file
        if path is None:
            return self.save_file_as()
        try:
            content = self.text.get("1.0", "end-1c")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.current_file = path
            self.modified = False
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
            return False

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".zap",
            filetypes=[("Zap files", "*.zap"), ("All files", "*.*")],
            initialdir=str(EXAMPLES_DIR)
        )
        if path:
            return self.save_file(path)
        return False

    def new_file(self):
        if self.modified:
            if not messagebox.askyesno("Unsaved Changes", "Discard unsaved changes?"):
                return
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.modified = False

    def get_code(self):
        return self.text.get("1.0", "end-1c")

    def set_code(self, code):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)
        self._highlight()
        self._redraw_lines()

    def get_selection(self):
        try:
            return self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return ""


# ════════════════════════════════════════════════════════════════════
# Output Console
# ════════════════════════════════════════════════════════════════════

class OutputConsole(ctk.CTkFrame):
    """Rich output console with ANSI color support."""
    
    ANSI_COLORS = {
        '30': COLORS["fg_muted"], '31': COLORS["error"], '32': COLORS["success"], 
        '33': COLORS["warning"], '34': COLORS["accent"], '35': "#c586c0",
        '36': "#4ec9b0", '37': COLORS["fg"],
        '90': COLORS["fg_muted"], '91': "#f85149", '92': "#3fb950", '93': COLORS["warning"],
        '96': "#4ec9b0", '97': COLORS["fg"],
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["code_bg"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        
        self.output_queue = queue.Queue()
        self._build_ui()
        self.after(50, self._process_queue)
        
    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        toolbar.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(toolbar, text="Console Output", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        self.auto_scroll = ctk.BooleanVar(value=True)
        ModernButton(toolbar, text="Clear", variant="ghost", width=70, command=self.clear).pack(side="right", padx=4)
        ModernButton(toolbar, text="Copy", variant="ghost", width=70, command=self.copy_all).pack(side="right", padx=4)
        ctk.CTkSwitch(toolbar, text="Auto-scroll", variable=self.auto_scroll, width=80).pack(side="right", padx=8)
        
        # Text area
        self.text = tk.Text(
            self,
            bg=COLORS["code_bg"],
            fg=COLORS["fg"],
            font=("JetBrains Mono", 11) if self._font_exists("JetBrains Mono") else ("Consolas", 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
            padx=12, pady=10,
        )
        self.text.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        
        # ANSI tags
        for code, color in self.ANSI_COLORS.items():
            self.text.tag_configure(f"ansi_{code}", foreground=color)
        self.text.tag_configure("stdout", foreground=COLORS["fg"])
        self.text.tag_configure("stderr", foreground=COLORS["error"])
        self.text.tag_configure("system", foreground=COLORS["accent"])
        self.text.tag_configure("success", foreground=COLORS["success"])
        self.text.tag_configure("prompt", foreground=COLORS["accent"], font=("JetBrains Mono", 11, "bold"))
        
        # Scrollbar
        v_scroll = ctk.CTkScrollbar(self, command=self.text.yview)
        v_scroll.grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 8))
        self.text.configure(yscrollcommand=v_scroll.set)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def _font_exists(self, name):
        import tkinter.font as tkfont
        return name in tkfont.families()

    def write(self, text, msg_type="stdout"):
        self.output_queue.put((msg_type, text))

    def _process_queue(self):
        try:
            while True:
                msg_type, content = self.output_queue.get_nowait()
                self._append(content, msg_type)
        except queue.Empty:
            pass
        self.after(50, lambda: self._process_queue())

    def _append(self, text, msg_type="stdout"):
        self.text.configure(state=tk.NORMAL)
        
        # Parse ANSI codes
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
                        if code in self.ANSI_COLORS:
                            tags.append(f"ansi_{code}")
                    current_tags = tuple(tags) if tags else ()
            else:
                if part:
                    tags = current_tags if current_tags else (msg_type,)
                    self.text.insert(tk.END, part, tags)
        
        if self.auto_scroll.get():
            self.text.see(tk.END)
        self.text.configure(state=tk.DISABLED)

    def clear(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.configure(state=tk.DISABLED)

    def copy_all(self):
        self.clipboard_clear()
        self.clipboard_append(self.text.get("1.0", tk.END))


# ════════════════════════════════════════════════════════════════════
# Parameter Panel
# ════════════════════════════════════════════════════════════════════

class ParameterPanel(ModernScrollableFrame):
    """Dynamic parameter controls for simulations."""
    
    def __init__(self, master, on_apply=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_apply = on_apply
        self.param_vars = {}
        self._build_ui()
        
    def _build_ui(self):
        # Preset selector
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(header, text="Simulation Parameters", font=ctk.CTkFont(weight="bold", size=14)).pack(side="left")
        
        self.preset_var = ctk.StringVar(value="Custom")
        ctk.CTkComboBox(
            self, values=["Custom", "Orbital", "Rocket", "Flight", "Structural", "Chemistry"],
            variable=self.preset_var, width=140, command=self._load_preset
        ).pack(anchor="e", pady=(0, 16))
        
        # Parameter sections
        sections = [
            ("⏱  Time", [
                ("dt", "Time Step (dt)", 0.001, 1.0, 0.01, 0.001),
                ("max_time", "Max Time (s)", 1.0, 1000.0, 10.0, 1.0),
            ]),
            ("🌍  Orbital", [
                ("mu", "μ (m³/s²)", 1e10, 1e15, 3.986e14, 1e11),
                ("r1", "Initial Radius (m)", 1e6, 1e11, 6.571e6, 1e6),
                ("r2", "Target Radius (m)", 1e6, 1e11, 4.2157e7, 1e6),
            ]),
            ("🚀  Rocket / Flight", [
                ("mass", "Mass (kg)", 100, 1e6, 84000, 1000),
                ("thrust", "Thrust (N)", 1e4, 1e7, 8.45e5, 1e4),
                ("isp", "Isp (s)", 100, 500, 311, 1),
                ("propellant", "Propellant (kg)", 100, 5e5, 40000, 1000),
            ]),
            ("🏗  Structural", [
                ("E", "Young's Modulus (Pa)", 1e9, 1e12, 2e11, 1e9),
                ("I", "Moment of Inertia", 1e-6, 1e-2, 8.33e-6, 1e-6),
                ("L", "Length (m)", 0.1, 100.0, 5.0, 0.1),
                ("load", "Load (N)", 100, 1e6, 10000, 100),
            ]),
            ("⚗️  Chemistry", [
                ("k", "Rate Constant", 0.001, 10.0, 0.1, 0.001),
                ("order", "Reaction Order", 0, 3, 1, 1),
                ("A0", "Initial [A]", 0.01, 10.0, 1.0, 0.01),
                ("B0", "Initial [B]", 0.01, 10.0, 2.0, 0.01),
            ]),
            ("🌐  General", [
                ("gravity", "Gravity (m/s²)", 0.0, 20.0, 9.81, 0.1),
            ]),
        ]
        
        for section_title, params in sections:
            self._add_section(section_title, params)
        
        # Apply button
        ctk.CTkButton(self, text="Apply to Visualization", height=40, 
                     font=ctk.CTkFont(weight="bold"), command=self._apply).pack(fill="x", pady=(16, 0))
        
    def _add_section(self, title, params):
        # Section header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(12, 4))
        ctk.CTkLabel(header, text=title, font=ctk.CTkFont(weight="bold", size=12), text_color=COLORS["accent"]).pack(anchor="w")
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=(0, 8))
        
        for name, label, min_v, max_v, default, step in params:
            self._add_param(name, label, min_v, max_v, default, step)
            
    def _add_param(self, name, label, min_v, max_v, default, step):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame, text=label, width=180, anchor="w").grid(row=0, column=0, padx=(0, 8))
        
        var = ctk.DoubleVar(value=default)
        self.param_vars[name] = var
        
        # Slider for continuous, entry for discrete
        if isinstance(step, int) and step >= 1:
            slider = ctk.CTkSlider(self, from_=min_v, to=max_v, variable=var, number_of_steps=int((max_v-min_v)/step))
            slider.pack(fill="x", padx=(0, 8))
        else:
            slider = ctk.CTkSlider(self, from_=min_v, to=max_v, variable=var)
            slider.pack(fill="x", padx=(0, 8))
        
        entry = ctk.CTkEntry(self, textvariable=var, width=80, justify="right")
        entry.pack(side="right", padx=(8, 0))

    def _load_preset(self, preset):
        presets = {
            "Orbital": {"dt": 0.01, "max_time": 100, "mu": 3.986e14, "r1": 6.571e6, "r2": 4.2157e7, "gravity": 0},
            "Rocket": {"dt": 0.1, "max_time": 400, "mass": 84000, "thrust": 8.45e5, "isp": 311, "propellant": 40000},
            "Flight": {"dt": 0.1, "max_time": 120, "mass": 1230, "thrust": 50000, "isp": 300, "gravity": 9.81},
            "Structural": {"dt": 1, "max_time": 1, "E": 2e11, "I": 8.33e-6, "L": 5, "load": 10000},
            "Chemistry": {"dt": 0.1, "max_time": 50, "k": 0.1, "order": 1, "A0": 1.0, "B0": 2.0},
        }
        if preset in presets:
            for k, v in presets[preset].items():
                if k in self.param_vars:
                    self.param_vars[k].set(v)

    def get_params(self):
        return {k: v.get() for k, v in self.param_vars.items()}

    def _apply(self):
        if self.on_apply:
            self.on_apply(self.get_params())


# ════════════════════════════════════════════════════════════════════
# Demo Browser
# ════════════════════════════════════════════════════════════════════

class DemoBrowser(ctk.CTkFrame):
    def __init__(self, master, on_load, on_run, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_load = on_load
        self.on_run = on_run
        self._build_ui()
        
    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Search
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 8))
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter)
        ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="🔍 Search demos...", 
                    font=ctk.CTkFont(size=13)).pack(fill="x")
        
        # Tree
        self.tree = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.tree.pack(fill="both", expand=True, pady=(8, 0))
        
        self.demo_cards = {}
        for key, (name, path, desc) in DEMOS.items():
            self._add_demo_card(key, name, path, desc)
            
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(12, 0))
        ctk.CTkButton(btn_frame, text="Load", command=self._load, height=36).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ctk.CTkButton(btn_frame, text="Run", fg_color=COLORS["success"], hover_color="#3fb950",
                     command=self._run, height=36).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def _add_demo_card(self, key, name, path, desc):
        frame = ctk.CTkFrame(self.tree, fg_color=COLORS["panel"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        frame.pack(fill="x", pady=4, padx=4)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame, text=name, font=ctk.CTkFont(weight="bold", size=13)).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(frame, text=desc, text_color=COLORS["fg_secondary"], font=ctk.CTkFont(size=11)).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        
        frame.bind("<Button-1>", lambda e, k=key: self._select(k))
        for child in frame.winfo_children():
            child.bind("<Button-1>", lambda e, k=key: self._select(k))
        
        self.demo_cards[key] = frame

    def _select(self, key):
        for k, card in self.demo_cards.items():
            card.configure(border_color=COLORS["accent"] if k == key else COLORS["border"])
        self.selected_key = key

    def _filter(self, *args):
        query = self.search_var.get().lower()
        for key, (name, _, desc) in DEMOS.items():
            match = query in name.lower() or query in desc.lower()
            # Just show/hide logic would go here

    def _load(self):
        if hasattr(self, 'selected_key'):
            self.on_load(self.selected_key)

    def _run(self):
        if hasattr(self, 'selected_key'):
            self.on_run(self.selected_key)


# ════════════════════════════════════════════════════════════════════
# Visualization Canvas
# ════════════════════════════════════════════════════════════════════

class VizCanvas(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["code_bg"], corner_radius=10, border_width=1, border_color=COLORS["border"], **kwargs)
        self.params = {}
        self._build_ui()
        
    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        
        ctk.CTkLabel(toolbar, text="Visualization", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        self.plot_type = ctk.StringVar(value="particles")
        ctk.CTkComboBox(toolbar, values=["particles", "trajectories", "energy", "fields", "3d"],
                       variable=self.plot_type, width=120).pack(side="right", padx=8)
        ctk.CTkLabel(toolbar, text="Plot:").pack(side="right", padx=8)
        
        ModernButton(toolbar, text="Clear", variant="ghost", width=70, command=self.clear).pack(side="right", padx=4)
        ModernButton(toolbar, text="Export", variant="ghost", width=70, command=self.export).pack(side="right", padx=4)
        
        # Matplotlib
        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor=COLORS["code_bg"])
        self.ax = self.fig.add_subplot(111)
        self._style_axes()
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        
        # Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        toolbar.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))
        toolbar.config(background=COLORS["code_bg"])
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._draw_placeholder()
        
    def _style_axes(self):
        self.ax.set_facecolor(COLORS["panel"])
        self.ax.tick_params(colors=COLORS["fg"], which='both')
        for spine in self.ax.spines.values():
            spine.set_color(COLORS["border"])
        self.ax.xaxis.label.set_color(COLORS["fg"])
        self.ax.yaxis.label.set_color(COLORS["fg"])
        self.ax.title.set_color(COLORS["accent"])
        self.fig.set_facecolor(COLORS["code_bg"])
        
    def _draw_placeholder(self):
        self.ax.clear()
        self.ax.set_facecolor(COLORS["panel"])
        self.ax.text(0.5, 0.5, "Run a simulation to visualize", 
                    ha='center', va='center', color=COLORS["fg_muted"], fontsize=14,
                    transform=self.ax.transAxes)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.fig.canvas.draw()
        
    def clear(self):
        self.ax.clear()
        self._style_axes()
        self._draw_placeholder()
        
    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")])
        if path:
            self.fig.savefig(path, dpi=300, facecolor=self.fig.get_facecolor())
            
    def set_params(self, params):
        pass

    def plot_particles(self, positions, colors=None, sizes=None, trails=None):
        self.ax.clear()
        self._style_axes()
        
        positions = np.array(positions)
        if len(positions) == 0:
            self._draw_placeholder()
            return
            
        if colors is None:
            colors = [COLORS["accent"]] * len(positions)
        if sizes is None:
            sizes = [50] * len(positions)
            
        self.ax.scatter(positions[:, 0], positions[:, 1], c=colors, s=sizes, alpha=0.8)
        
        if trails:
            for trail in trails:
                trail = np.array(trail)
                if len(trail) > 1:
                    self.ax.plot(trail[:, 0], trail[:, 1], '-', color=COLORS["accent"], alpha=0.3, linewidth=1)
                    
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.margins(0.1)
        self.fig.canvas.draw()
        
    def plot_trajectories(self, trajectories, labels=None):
        self.ax.clear()
        self._style_axes()
        
        for i, traj in enumerate(trajectories):
            traj = np.array(traj)
            if len(traj) > 1:
                color = plt.cm.tab10(i % 10)
                self.ax.plot(traj[:, 0], traj[:, 1], '-', color=color, linewidth=1.5, 
                           label=labels[i] if labels else f"Traj {i+1}")
                
        self.ax.legend(loc='upper right', fontsize=8)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.margins(0.1)
        self.fig.canvas.draw()
        
    def plot_energy(self, time, energies, labels=None):
        self.ax.clear()
        self._style_axes()
        
        for i, energy in enumerate(energies):
            label = labels[i] if labels and i < len(labels) else f"Energy {i+1}"
            self.ax.plot(time, energy, '-', label=label, linewidth=1.5)
            
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Energy (J)")
        self.ax.legend(loc='upper right', fontsize=8)
        self.ax.grid(True, alpha=0.3)
        self.fig.canvas.draw()
        
    def plot_3d(self, positions, colors=None):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self._style_axes_3d()
        
        positions = np.array(positions)
        if colors is None:
            colors = [COLORS["accent"]] * len(positions)
            
        self.ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                       c=colors, s=30, alpha=0.8)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.canvas.draw()
        
    def _style_axes_3d(self):
        self.ax.set_facecolor(COLORS["panel"])
        for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:
            axis.set_tick_params(colors=COLORS["fg"])
            axis.label.set_color(COLORS["fg"])
            axis._axinfo['grid']['color'] = COLORS["border"]
        self.fig.set_facecolor(COLORS["code_bg"])
        
    def set_params(self, params):
        pass


# ════════════════════════════════════════════════════════════════════
# Simulation Controller
# ════════════════════════════════════════════════════════════════════

class SimController(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color=COLORS["panel"], corner_radius=10, border_width=1, border_color=COLORS["border"], height=60, **kwargs)
        self.app = app
        self.running = False
        self._build_ui()
        
    def _build_ui(self):
        self.pack_propagate(False)
        self.grid_columnconfigure(4, weight=1)
        
        # Restart
        ModernButton(self, text="⏮", width=44, height=36, variant="secondary", command=self.app.restart_sim).pack(side="left", padx=8, pady=12)
        
        # Play/Pause
        self.play_btn = ModernButton(self, text="▶", width=44, height=36, variant="primary", command=self._toggle)
        self.play_btn.pack(side="left", padx=4, pady=12)
        
        # Stop
        ModernButton(self, text="■", width=44, height=36, variant="secondary", command=self.app.stop_sim).pack(side="left", padx=4, pady=12)
        
        # Step
        ModernButton(self, text="⏭", width=44, height=36, variant="secondary", command=self._step).pack(side="left", padx=4, pady=12)
        
        # Separator
        ctk.CTkFrame(self, width=1, fg_color=COLORS["border"]).pack(side="left", fill="y", padx=12, pady=8)
        
        # Speed
        ctk.CTkLabel(self, text="Speed:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(12, 4))
        self.speed_var = ctk.DoubleVar(value=1.0)
        speed_slider = ctk.CTkSlider(self, from_=0.1, to=10.0, variable=self.speed_var, 
                                    width=140, command=self._on_speed)
        speed_slider.pack(side="left", padx=4)
        self.speed_label = ctk.CTkLabel(self, text="1.0×", width=40, font=ctk.CTkFont(weight="bold"))
        self.speed_label.pack(side="left", padx=4)
        
        # Frame counter
        self.frame_var = ctk.StringVar(value="Frame: 0")
        ctk.CTkLabel(self, textvariable=self.frame_var, text_color=COLORS["accent"], 
                    font=ctk.CTkFont(weight="bold")).pack(side="left", padx=20)
        
        # Time
        self.time_var = ctk.StringVar(value="Time: 0.00s")
        ctk.CTkLabel(self, textvariable=self.time_var, text_color=COLORS["fg_muted"]).pack(side="left", padx=8)
        
    def _toggle(self):
        if self.running:
            self.running = False
            self.play_btn.configure(text="▶")
        else:
            self.running = True
            self.play_btn.configure(text="⏸")
            self.app.run_current()
            
    def _step(self):
        pass
        
    def _on_speed(self, val):
        self.speed = float(val)
        self.speed_label.configure(text=f"{self.speed:.1f}×")
        
    def update_state(self):
        if hasattr(self.app, 'sim_thread') and self.app.sim_thread and self.app.sim_thread.is_alive():
            if not self.running:
                self.running = True
                self.play_btn.configure(text="⏸")
        else:
            if self.running:
                self.running = False
                self.play_btn.configure(text="▶")


# ════════════════════════════════════════════════════════════════════
# Demo Browser (Sidebar)
# ════════════════════════════════════════════════════════════════════

class DemoSidebar(ctk.CTkFrame):
    def __init__(self, master, on_load, on_run, **kwargs):
        super().__init__(master, width=300, fg_color=COLORS["panel"], corner_radius=0, border_width=0, **kwargs)
        self.on_load = on_load
        self.on_run = on_run
        self.pack_propagate(False)
        self._build_ui()
        
    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=16)
        ctk.CTkLabel(header, text="Built-in Demos", font=ctk.CTkFont(weight="bold", size=14)).pack(side="left")
        
        # Search
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter)
        ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="🔍 Search...", 
                    height=36).pack(fill="x", padx=12, pady=(0, 12))
        
        # Demo list
        self.scroll = ModernScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))
        
        self.demo_cards = {}
        self.selected_key = None
        for key, (name, path, desc) in DEMOS.items():
            self._add_card(key, name, desc)

    def _filter(self, *args):
        query = self.search_var.get().lower()
        for key, (name, _, desc) in DEMOS.items():
            match = query in name.lower() or query in desc.lower()
            # Visibility logic here

    def _add_card(self, key, name, desc):
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS["panel"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=4, padx=4)
        card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(weight="bold", size=13)).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(card, text=desc, text_color=COLORS["fg_secondary"], font=ctk.CTkFont(size=11), wraplength=240).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        
        card.bind("<Button-1>", lambda e, k=key: self._select(k))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, k=key: self._select(k))
        
        self.demo_cards[key] = card

    def _filter(self, *args):
        query = self.search_var.get().lower()
        for key, (name, _, desc) in DEMOS.items():
            match = query in name.lower() or query in desc.lower()
            # Visibility logic here

    def _select(self, key):
        for k, card in self.demo_cards.items():
            card.configure(border_color=COLORS["accent"] if k == key else COLORS["border"])
        self.selected = key

    def _load(self):
        if hasattr(self, 'selected'):
            self.on_load(self.selected)

    def _run(self):
        if hasattr(self, 'selected'):
            self.on_run(self.selected)


# ════════════════════════════════════════════════════════════════════
# Main Application
# ════════════════════════════════════════════════════════════════════

class ZapPhysicsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ZapPhysics v4.1 — Physics + Chemistry + Engineering")
        self.geometry("1700x1050")
        self.minsize(1300, 850)
        
        # State
        self.sim_thread = None
        self.sim_queue = queue.Queue()
        self.running = False
        
        # Build UI
        self._setup_layout()
        self._create_menu()
        self._bind_shortcuts()
        self._load_welcome()
        
    def _setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        
        # Left: Sidebar (Demos)
        self.sidebar = DemoSidebar(self, self._load_demo, self._run_demo)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # Center: Editor + Viz
        self.center_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.center_pane.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        self.center_pane.grid_rowconfigure(0, weight=1)
        self.center_pane.grid_columnconfigure(0, weight=1)
        self.center_pane.grid_rowconfigure(1, weight=1)
        
        # Editor
        editor_frame = ctk.CTkFrame(self.center_pane, fg_color=COLORS["panel"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        editor_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        editor_frame.grid_rowconfigure(1, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        # Editor toolbar
        toolbar = ctk.CTkFrame(editor_frame, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        
        ModernButton(toolbar, text="▶ Run", command=self.run_current, width=100).pack(side="left", padx=2)
        ModernButton(toolbar, text="■ Stop", variant="secondary", command=self.stop_sim, width=100).pack(side="left", padx=2)
        ModernButton(toolbar, text="↻ Restart", variant="ghost", width=90, command=self.restart_sim).pack(side="left", padx=2)
        
        ctk.CTkLabel(toolbar, text="").pack(side="left", expand=True)
        
        ModernButton(toolbar, text="📁 Open", variant="secondary", command=self.open_file, width=90).pack(side="right", padx=2)
        ModernButton(toolbar, text="💾 Save", variant="secondary", command=self.save_file, width=90).pack(side="right", padx=2)
        ModernButton(toolbar, text="➕ New", variant="ghost", width=90, command=self.new_file).pack(side="right", padx=2)
        
        self.editor = CodeEditor(editor_frame)
        self.editor.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.editor.on_save = self.save_file
        
        # Visualization
        self.viz = VizCanvas(self.center_pane)
        self.viz.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        
        # Right: Parameters + Console
        self.right_pane = ctk.CTkFrame(self, fg_color="transparent", width=380)
        self.right_pane.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(4, 8), pady=8)
        self.right_pane.pack_propagate(False)
        self.right_pane.configure(width=380)
        self.right_pane.grid_rowconfigure(0, weight=1)
        self.right_pane.grid_rowconfigure(1, weight=1)
        self.right_pane.grid_columnconfigure(0, weight=1)
        
        # Parameters
        self.params = ParameterPanel(self.right_pane, on_apply=self.viz.set_params)
        self.params.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        
        # Console
        self.console = OutputConsole(self.right_pane)
        self.console.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        
        # Bottom: Controller
        self.controller = SimController(self, self)
        self.controller.grid(row=2, column=1, columnspan=2, sticky="ew", padx=8, pady=(0, 8))
        
    def _create_menu(self):
        menubar = tk.Menu(self, bg=COLORS["panel"], fg=COLORS["fg"], 
                         activebackground=COLORS["accent"], activeforeground="#fff", border=0)
        self.config(menu=menubar)
        
        # File
        file_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["panel"], fg=COLORS["fg"],
                           activebackground=COLORS["accent"], activeforeground="#fff", border=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Examples...", command=self._show_examples, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        
        # Run
        run_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["panel"], fg=COLORS["fg"],
                          activebackground=COLORS["accent"], activeforeground="#fff", border=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Current", command=self.run_current, accelerator="F5")
        run_menu.add_command(label="Run Selection", command=self.run_selection, accelerator="F9")
        run_menu.add_separator()
        run_menu.add_command(label="Stop", command=self.stop_sim, accelerator="Shift+F5")
        run_menu.add_command(label="Restart", command=self.restart_sim, accelerator="Ctrl+F5")
        run_menu.add_separator()
        run_menu.add_command(label="Run All Demos", command=self._run_all_demos)
        
        # View
        view_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["panel"], fg=COLORS["fg"],
                           activebackground=COLORS["accent"], activeforeground="#fff", border=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Console", command=self._toggle_console)
        view_menu.add_command(label="Toggle Parameters", command=self._toggle_params)
        view_menu.add_separator()
        view_menu.add_command(label="Reset Layout", command=self._reset_layout)
        
        # Help
        help_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["panel"], fg=COLORS["fg"],
                           activebackground=COLORS["accent"], activeforeground="#fff", border=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Zap Language Reference", command=self._open_docs)
        help_menu.add_command(label="GitHub Repository", command=lambda: webbrowser.open("https://github.com/M-2000-0/ZAPphysics"))
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about)
        
    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-Shift-S>", lambda e: self.save_file_as())
        self.bind("<Control-e>", lambda e: self._show_examples())
        self.bind("<F5>", lambda e: self.run_current())
        self.bind("<F9>", lambda e: self.run_selection())
        self.bind("<Shift-F5>", lambda e: self.stop_sim())
        self.bind("<Control-F5>", lambda e: self.restart_sim())
        self.bind("<Control-q>", lambda e: self.quit())
        
    def _load_welcome(self):
        welcome = """# ZapPhysics v4.1 — Modern Physics Engine IDE

Welcome! Select a demo from the sidebar or create a new script.

## Quick Start
1. **Browse demos** → Click any demo in the sidebar to load
2. **Run** → Press F5 or click ▶ Run
3. **Tune** → Adjust parameters in the right panel
3. **Visualize** → Watch real-time plots in the visualization pane

## Keyboard Shortcuts
| Key | Action |
|-----|--------|
| F5 | Run script |
| F9 | Run selection |
| Shift+F5 | Stop |
| Ctrl+F5 | Restart |
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save |
| Ctrl+E | Open examples |

## Zap Language Quick Reference
```
fn gravity(m1, m2, r)  m1 * m2 / (r * r)  # Function
let G = 6.674e-11      # Constant
for i in range(100):   # Loop
  let f = gravity(m1, m2, r)
```

Happy simulating! 🚀
"""
        self.editor.set_code(welcome)
        
    # ─── File Operations ───
    def new_file(self):
        if self.editor.modified and not messagebox.askyesno("Unsaved Changes", "Discard unsaved changes?"):
            return
        self.editor.new_file()
        
    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Zap files", "*.zap"), ("All files", "*.*")],
            initialdir=str(EXAMPLES_DIR)
        )
        if path:
            self.editor.load_file(path)
            
    def save_file(self):
        return self.editor.save_file()
        
    def save_file_as(self):
        return self.editor.save_file_as()
        
    def _show_examples(self):
        """Show examples dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Open Example")
        dialog.geometry("500x500")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Select Example", font=ctk.CTkFont(weight="bold", size=16)).pack(pady=16)
        
        list_frame = ctk.CTkScrollableFrame(dialog)
        list_frame.pack(fill="both", expand=True, padx=16, pady=16)
        
        for key, (name, path, desc) in DEMOS.items():
            frame = ctk.CTkFrame(list_frame, fg_color=COLORS["panel"], corner_radius=8)
            frame.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(frame, text=name, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(frame, text=desc, text_color=COLORS["fg_secondary"], wraplength=300).pack(anchor="w", padx=12, pady=(0, 8))
            
            def make_loader(p):
                return lambda: (self.editor.load_file(p), dialog.destroy())
            ctk.CTkButton(frame, text="Load", width=80, command=make_loader(os.path.join(EXAMPLES_DIR, key + ".zap"))).pack(side="right", padx=12, pady=8)

    def _load_demo(self, key):
        """Load a built-in demo."""
        demo = DEMOS.get(key)
        if not demo:
            return
        name, path, desc = demo
        full_path = os.path.join(EXAMPLES_DIR, path)
        if os.path.exists(full_path):
            self.editor.load_file(full_path)
            self.console.write_system(f">>> Loaded demo: {name}\n")
        else:
            # Try lib
            lib_path = os.path.join(ROOT, "lib", key + ".zap")
            if os.path.exists(lib_path):
                self.editor.load_file(lib_path)
                self.console.write_system(f">>> Loaded lib: {name}\n")

    def _run_demo(self, key):
        self._load_demo(key)
        self.run_current()
        
    def _run_all_demos(self):
        self.console.clear()
        self.console.write_system(">>> Running all 22 demos...\n\n")
        main_path = ROOT / "main.zap"
        if main_path.exists():
            self._run_file_async(str(main_path))
        else:
            messagebox.showerror("Error", "main.zap not found in project root")
            
    # ─── Run Operations ───
    def run_current(self):
        code = self.editor.get_code()
        if not code.strip():
            return
        self._run_code_async(code)
        
    def run_selection(self):
        code = self.editor.get_selection()
        if not code.strip():
            messagebox.showinfo("No Selection", "No code selected.")
            return
        self._run_code_async(code)
        
    def _run_code_async(self, code):
        self.console.clear()
        self.console.write(f">>> Running...\n\n", "system")
        self.controller.running = True
        self.controller.play_btn.configure(text="⏸")
        
        def run():
            # Write to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.zap', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = str(ZAP_SRC) + os.pathsep + env.get('PYTHONPATH', '')
                
                proc = subprocess.Popen(
                    [sys.executable, "-m", "zap", "run", temp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=str(ROOT),
                    env=env
                )
                
                for line in iter(proc.stdout.readline, ''):
                    if line:
                        self.sim_queue.put(("stdout", line))
                proc.wait()
                
                if proc.returncode == 0:
                    self.sim_queue.put(("success", f"\n>>> Exit code: {proc.returncode}\n"))
                else:
                    self.sim_queue.put(("stderr", f"\n>>> Exit code: {proc.returncode}\n"))
                    
            except Exception as e:
                self.sim_queue.put(("stderr", f"Error: {e}\n"))
            finally:
                try:
                    os.unlink(temp_path)
                except:
                    pass
                self.sim_queue.put(("done", None))
                
        self.sim_thread = threading.Thread(target=run, daemon=True)
        self.sim_thread.start()
        self.after(50, self._process_sim_queue)
        
    def _run_file_async(self, path):
        self.console.clear()
        self.console.write_system(f">>> Running: {os.path.basename(path)}\n\n")
        
        def run():
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = str(ZAP_SRC) + os.pathsep + env.get('PYTHONPATH', '')
                
                proc = subprocess.Popen(
                    [sys.executable, "-m", "zap", "run", path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=str(ROOT),
                    env=env
                )
                
                for line in iter(proc.stdout.readline, ''):
                    if line:
                        self.sim_queue.put(("stdout", line))
                proc.wait()
                
                if proc.returncode == 0:
                    self.sim_queue.put(("success", f"\n>>> Exit code: {proc.returncode}\n"))
                else:
                    self.sim_queue.put(("stderr", f"\n>>> Exit code: {proc.returncode}\n"))
                    
            except Exception as e:
                self.sim_queue.put(("stderr", f"Error: {e}\n"))
            finally:
                self.sim_queue.put(("done", None))
                
        self.sim_thread = threading.Thread(target=run, daemon=True)
        self.sim_thread.start()
        self.after(50, self._process_sim_queue)
        
    def _process_sim_queue(self):
        try:
            while True:
                msg_type, content = self.sim_queue.get_nowait()
                if msg_type == "stdout":
                    self.console.write(content, "stdout")
                elif msg_type == "stderr":
                    self.console.write(content, "stderr")
                elif msg_type == "success":
                    self.console.write(content, "success")
                elif msg_type == "done":
                    self.controller.running = False
                    self.controller.play_btn.configure(text="▶")
                    return
        except queue.Empty:
            pass
        self.after(50, self._process_sim_queue)
        
    def stop_sim(self):
        if self.sim_thread and self.sim_thread.is_alive():
            # Can't easily kill subprocess, but we can stop waiting
            self.controller.running = False
            self.controller.play_btn.configure(text="▶")
            self.console.write_system("\n>>> Stop requested\n")
            
    def restart_sim(self):
        self.stop_sim()
        self.after(200, self.run_current)
        
    def _toggle_console(self):
        pass
        
    def _toggle_params(self):
        pass
        
    def _reset_layout(self):
        pass
        
    def _open_docs(self):
        webbrowser.open("https://github.com/M-2000-0/ZAPphysics/blob/main/README.md")
        
    def _show_about(self):
        messagebox.showinfo("About ZapPhysics v4.1",
            "ZapPhysics v4.1\n\n"
            "Physics + Chemistry + Engineering + Aerospace\n"
            "22 demos: N-body, collision, chemistry, EM, SPH, rigid body,\n"
            "structural, game, broadphase, rocket, aero, orbital, flight.\n\n"
            "Language: Zap (custom Python-interpreted DSL)\n"
            "GUI: CustomTkinter + Matplotlib\n\n"
            "GitHub: https://github.com/M-2000-0/ZAPphysics")


def main():
    app = ZapPhysicsApp()
    app.mainloop()


if __name__ == "__main__":
    main()