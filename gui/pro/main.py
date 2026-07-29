"""
ZapPhysics Professional — Main Application
Modern CustomTkinter-based IDE with professional architecture.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import sys
import threading
import queue
import subprocess
import webbrowser
from pathlib import Path
import time

# Internal imports
from .settings import SettingsManager, AppSettings, get_settings_manager
from .theme import ThemeManager, get_theme_manager, ThemeColors
from .state import EventBus, StateManager, EventType, get_event_bus, get_state_manager, initialize_state
from .widgets import *
from .editor import ZapSyntaxHighlighter, CodeEditor
from .console import OutputConsole, _Redirector
from .viz_canvas import VizCanvas, SimController, DemoBrowser
from .param_panel import ParameterPanel
from .widgets import *

# Constants
ROOT = Path(__file__).parent.parent.parent
ZAP_SRC = ROOT / "zap" / "src"
EXAMPLES_DIR = ROOT / "examples"

sys.path.insert(0, str(ZAP_SRC))


# ═══════════════════════════════════════════════════════════════════════════════════
# Demo Catalog
# ═══════════════════════════════════════════════════════════════════════════════════

DEMOS = {
    "orbital": ("Orbital Mechanics", "examples/demo_orbital.zpx", "N-body gravity, Hohmann transfers"),
    "orbital3d": ("3D Orbital (VV)", "examples/demo_orbital3d.zpx", "3D velocity verlet integration"),
    "lambert": ("Lambert Solver", "examples/demo_lambert.zpx", "Orbital targeting & rendezvous"),
    "porkchop": ("Porkchop Plot", "examples/demo_porkchop.zpx", "Earth→Mars launch windows"),
    "rocket": ("Rocket Engineering", "examples/demo_rocket.zpx", "Multi-stage design & trajectory"),
    "flight": ("Flight Dynamics", "examples/demo_flight.zpx", "Aircraft aerodynamics & envelope"),
    "structural": ("Structural Eng", "examples/demo_structural.zpx", "Truss & beam analysis"),
    "game": ("Game Physics", "examples/demo_game.zpx", "Platformer, top-down, ragdoll"),
    "collisions": ("Collisions", "examples/collisions.zpx", "Elastic collision dynamics"),
    "springs": ("Spring-Mass", "examples/springs.zpx", "Oscillator systems"),
    "chemistry": ("Chemistry Lab", "examples/chemistry.zpx", "Molecules, reactions, thermo"),
    "elements": ("Periodic Table", "examples/demo_elements.zpx", "118 elements"),
    "kinetics": ("Kinetics", "examples/demo_kinetics.zpx", "Rate laws, equilibrium, enzymes"),
    "em": ("Electromagnetics", "examples/demo_em.zpx", "Coulomb, Lorentz, fields"),
    "fluid": ("SPH Fluids", "examples/demo_fluid.zpx", "Smoothed particle hydrodynamics"),
    "rigid": ("Rigid Body", "examples/demo_rigid.zpx", "Rotation, torque, inertia"),
    "tensor": ("Tensor N-Body", "examples/tensor.zpx", "Matrix force calculations"),
    "visual": ("ASCII Viz", "examples/demo_visual.zpx", "Charts, sparklines, heatmaps"),
    "art": ("Generative Art", "examples/demo_art.zpx", "Particle fountains, spirals"),
    "broadphase": ("Broadphase", "examples/demo_broadphase.zpx", "Grid & quadtree collision"),
    "constraints": ("Constraints", "examples/demo_constraints.zpx", "Distance, spring, hinge, slider"),
}


# ═══════════════════════════════════════════════════════════════════════════════════
# Main Application
# ═══════════════════════════════════════════════════════════════════════════════════

class ZapPhysicsApp(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize core systems
        self.settings_manager = SettingsManager()
        self.theme_manager = ThemeManager(self.settings_manager)
        self.event_bus = EventBus()
        self.state_manager = StateManager(self.event_bus)
        
        # Initialize theme
        self.theme_manager.initialize()
        
        # Configure window
        self.title("ZapPhysics Professional v4.2")
        self.geometry("1800x1080")
        self.minsize(1400, 900)
        
        # Load settings
        settings = self.settings_manager.load()
        self.geometry(settings.window_geometry)
        if settings.window_state == "maximized":
            self.state('zoomed')
            
        # State
        self.sim_thread = None
        self.sim_queue = queue.Queue()
        self.running = False
        self.current_file = None
        self.modified = False
        
        # Build UI
        self._setup_layout()
        self._create_menu()
        self._bind_shortcuts()
        self._load_welcome()
        
        # Start UI update loop
        self.after(30, self._update_ui)
        
    def _setup_layout(self):
        """Configure main layout with split panes."""
        # Configure main grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        
        # ─── Left: Demo Sidebar ───
        self.sidebar = self._create_sidebar()
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(8, 4), pady=8)
        
        # ─── Center: Editor + Visualization ───
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=1, sticky="nsew", padx=(4, 4), pady=8)
        center.grid_rowconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=1)
        center.grid_columnconfigure(0, weight=1)
        
        # Editor
        editor_frame = ProFrame(center, variant="card")
        editor_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        editor_frame.grid_rowconfigure(1, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        # Editor toolbar
        toolbar = ctk.CTkFrame(editor_frame, fg_color="transparent", height=44)
        toolbar.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        toolbar.grid_columnconfigure(2, weight=1)
        
        ProButton(toolbar, text="▶ Run", command=self.run_current, width=100).pack(side="left", padx=2)
        ProButton(toolbar, text="■ Stop", variant="secondary", command=self.stop_sim, width=100).pack(side="left", padx=2)
        ProButton(toolbar, text="↻ Restart", variant="ghost", width=90, command=self.restart_sim).pack(side="left", padx=2)
        
        ctk.CTkLabel(toolbar, text="").pack(side="left", expand=True)
        
        ProButton(toolbar, text="📁 Open", variant="secondary", command=self.open_file, width=90).pack(side="right", padx=2)
        ProButton(toolbar, text="💾 Save", variant="secondary", command=self.save_file, width=90).pack(side="right", padx=2)
        ProButton(toolbar, text="➕ New", variant="ghost", width=90, command=self.new_file).pack(side="right", padx=2)
        
        # Editor
        self.editor = CodeEditor(editor_frame)
        self.editor.on_save = self.save_file
        self.editor.on_run = self.run_current
        self.editor.on_content_changed = self._on_content_changed
        self.editor.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        
        # Visualization
        self.viz = VizCanvas(editor_frame)
        self.viz.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        
        # ─── Right: Parameters + Console ───
        right_pane = ctk.CTkFrame(self, fg_color="transparent", width=380)
        right_pane.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(4, 8), pady=8)
        right_pane.pack_propagate(False)
        right_pane.configure(width=380)
        right_pane.grid_rowconfigure(0, weight=1)
        right_pane.grid_rowconfigure(1, weight=1)
        right_pane.grid_columnconfigure(0, weight=1)
        
        # Parameters
        self.params = ParameterPanel(right_pane, on_apply=self.viz.set_params)
        self.params.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        
        # Console
        self.console = OutputConsole(right_pane)
        self.console.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        
        # ─── Bottom: Controller ───
        self.controller = SimController(self, self)
        self.controller.grid(row=2, column=1, columnspan=2, sticky="ew", padx=8, pady=(0, 8))
        
    def _create_sidebar(self) -> ctk.CTkFrame:
        """Create the demo sidebar."""
        sidebar = ProFrame(self, variant="panel", width=300)
        sidebar.pack_propagate(False)
        sidebar.configure(width=300)
        
        sidebar.grid_rowconfigure(1, weight=1)
        sidebar.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(sidebar, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
        
        ctk.CTkLabel(header, text="Built-in Demos", font=ctk.CTkFont(weight="bold", size=14)).pack(side="left")
        
        # Search
        self.sidebar_search = ctk.StringVar()
        self.sidebar_search.trace_add("write", self._filter_sidebar)
        ctk.CTkEntry(sidebar, textvariable=self.sidebar_search, placeholder_text="🔍 Search demos...", 
                    height=36).grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        
        # Demo list
        self.sidebar_scroll = ProScrollableFrame(sidebar)
        self.sidebar_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 12))
        
        self.sidebar_cards = {}
        self.selected_demo = None
        for key, (name, path, desc) in DEMOS.items():
            self._add_sidebar_card(key, name, path, desc)
            
        # Action buttons
        btn_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 16))
        
        ProButton(btn_frame, text="Load", command=self._load_selected, height=36).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ProButton(btn_frame, text="Run", fg_color="#3fb950", hover_color="#4ac45a", 
                 command=self._run_selected, height=36).pack(side="left", expand=True, fill="x", padx=(4, 0))
        
        return sidebar
        
    def _add_sidebar_card(self, key: str, name: str, path: str, desc: str):
        """Add a demo card to sidebar."""
        card = ProCard(self.sidebar_scroll, on_click=lambda k=key: self._select_demo(k))
        card.pack(fill="x", pady=4, padx=4)
        card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(weight="bold", size=13)).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(card, text=desc, text_color="#8b949e", font=ctk.CTkFont(size=11), wraplength=240).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        
        self.sidebar_cards[key] = card
        
    def _select_demo(self, key: str):
        for k, card in self.sidebar_cards.items():
            card.set_selected(k == key)
        self.selected_demo = key
        
    def _filter_sidebar(self, *args):
        query = self.sidebar_search.get().lower()
        for key, (name, _, desc) in DEMOS.items():
            card = self.sidebar_cards.get(key)
            if card:
                match = query in name.lower() or query in desc.lower()
                if match:
                    card.pack(fill="x", pady=4, padx=4)
                else:
                    card.pack_forget()
                    
    def _load_selected(self):
        if self.selected_demo:
            self._load_demo(self.selected_demo)
            
    def _run_selected(self):
        if self.selected_demo:
            self._load_demo(self.selected_demo)
            self.run_current()
            
    def _load_demo(self, key: str):
        demo = DEMOS.get(key)
        if not demo:
            return
        name, path, desc = demo
        full_path = ROOT / path
        if self.editor.load_file(full_path):
            self.console.write_system(f">>> Loaded demo: {name}\n")
            
    def _load_welcome(self):
        welcome = """# ZapPhysics Professional v4.2

Welcome to the professional physics simulation IDE.

## Quick Start
1. **Select a demo** from the sidebar → Click "Load" or double-click
2. **Run** → Press F5 or click ▶ Run
3. **Tune** → Adjust parameters in the right panel
4. **Visualize** → Watch real-time plots in the visualization pane

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
| Ctrl+Shift+S | Save as |
| Ctrl+E | Open examples |

## Zap Language Quick Reference
```
fn gravity(m1, m2, r)  m1 * m2 / (r * r)  # Function
let G = 6.674e-11       # Constant
for i in range(100):    # Loop
  let f = gravity(m1, m2, r)
```

## Built-in Functions
| Category | Functions |
|--------|-----------|
| Math | sin, cos, tan, sqrt, abs, floor, ceil, round, min, max, sum, random |
| Vector | Vec2, Vec3, Vec4, AABB, Particle, World, Quadtree, UniformGrid |
| I/O | say, show, print, len, range, map, filter, reduce |
| Time | now, wait, clear |

Happy simulating! 🚀
"""
        self.editor.set_code(welcome)
        
    # ═══════════════════════════════════════════════════════════════════════════════
    # File Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def new_file(self):
        if self.modified and not self._confirm_discard():
            return
        self.editor.new_file()
        
    def open_file(self):
        path = filedialog.askopenfilename(
            defaultextension=".zpx",
            filetypes=[("ZPX files", "*.zpx"), ("All files", "*.*")],
            initialdir=str(EXAMPLES_DIR)
        )
        if path:
            self.editor.load_file(path)
            
    def save_file(self):
        return self.editor.save_file()
        
    def save_as(self):
        return self.editor.save_as()
        
    def _confirm_discard(self) -> bool:
        return messagebox.askyesno(
            "Unsaved Changes",
            "You have unsaved changes. Discard them?",
            icon="warning"
        )
        
    # ═══════════════════════════════════════════════════════════════════════════════
    # Run Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
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
        
    def _run_code_async(self, code: str):
        self.console.clear()
        self.console.write(f">>> Running...\n\n", "system")
        self.running = True
        self.controller.play_btn.configure(text="⏸")
        self.controller.running = True
        
        def run():
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.zpx', delete=False) as f:
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
                elif msg_type == "stderr":
                    self.console.write(content, "stderr")
                elif msg_type == "done":
                    self.running = False
                    self.controller.running = False
                    self.controller.play_btn.configure(text="▶")
                    return
        except queue.Empty:
            pass
        if self.running:
            self.after(50, self._process_sim_queue)
            
    def stop_sim(self):
        if self.running:
            self.running = False
            self.controller.running = False
            self.controller.play_btn.configure(text="▶")
            self.console.write_system("\n>>> Stop requested\n")
            
    def restart_sim(self):
        self.stop_sim()
        self.after(200, self.run_current)
        
    # ═══════════════════════════════════════════════════════════════════════════════
    # UI Callbacks
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _on_content_changed(self, code: str):
        self.modified = True
        self.editor.modified = True
        self.editor._update_modified_indicator()
        
    def _update_ui(self):
        """Periodic UI update."""
        self.controller.update_state()
        self.after(50, self._update_ui)
        
    def _create_menu(self):
        menubar = tk.Menu(self, bg="#161b22", fg="#e6edf3", 
                         activebackground="#1f6feb", activeforeground="#fff", border=0)
        self.config(menu=menubar)
        
        # File
        file_menu = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#e6edf3",
                           activebackground="#1f6feb", activeforeground="#fff", border=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Examples...", command=self._show_examples, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        
        # Run
        run_menu = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#e6edf3",
                          activebackground="#1f6feb", activeforeground="#fff", border=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Current", command=self.run_current, accelerator="F5")
        run_menu.add_command(label="Run Selection", command=self.run_selection, accelerator="F9")
        run_menu.add_separator()
        run_menu.add_command(label="Stop", command=self.stop_sim, accelerator="Shift+F5")
        run_menu.add_command(label="Restart", command=self.restart_sim, accelerator="Ctrl+F5")
        run_menu.add_separator()
        run_menu.add_command(label="Run All Demos", command=self._run_all_demos)
        
        # View
        view_menu = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#e6edf3",
                           activebackground="#1f6feb", activeforeground="#fff", border=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Console", command=self._toggle_console)
        view_menu.add_command(label="Toggle Parameters", command=self._toggle_params)
        view_menu.add_separator()
        view_menu.add_command(label="Reset Layout", command=self._reset_layout)
        
        # Help
        help_menu = tk.Menu(menubar, tearoff=0, bg="#161b22", fg="#e6edf3",
                           activebackground="#1f6feb", activeforeground="#fff", border=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Zap Language Reference", command=self._open_docs)
        help_menu.add_command(label="GitHub Repository", command=lambda: webbrowser.open("https://github.com/M-2000-0/ZAPphysics"))
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about)
        
    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-Shift-S>", lambda e: self.save_as())
        self.bind("<Control-e>", lambda e: self._show_examples())
        self.bind("<F5>", lambda e: self.run_current())
        self.bind("<F9>", lambda e: self.run_selection())
        self.bind("<Shift-F5>", lambda e: self.stop_sim())
        self.bind("<Control-F5>", lambda e: self.restart_sim())
        self.bind("<Control-q>", lambda e: self.quit())
        
    def _show_examples(self):
        """Show examples dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Open Example")
        dialog.geometry("500x500")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Select Example", font=ctk.CTkFont(weight="bold", size=16)).pack(pady=16)
        
        list_frame = ProScrollableFrame(dialog)
        list_frame.pack(fill="both", expand=True, padx=16, pady=16)
        
        for key, (name, path, desc) in DEMOS.items():
            frame = ctk.CTkFrame(list_frame, fg_color="#161b22", corner_radius=8)
            frame.pack(fill="x", pady=4, padx=4)
            
            ctk.CTkLabel(frame, text=name, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(frame, text=desc, text_color="#8b949e", wraplength=300).pack(anchor="w", padx=12, pady=(0, 8))
            
            def make_loader(p):
                return lambda: (self.editor.load_file(str(ROOT / p)), dialog.destroy())
            ctk.CTkButton(frame, text="Load", width=80, command=make_loader(path)).pack(side="right", padx=12, pady=8)
            
    def _run_all_demos(self):
        self.console.clear()
        self.console.write_system(">>> Running all 22 demos...\n\n")
        main_file = ROOT / "main.zpx"
        if main_file.exists():
            self._run_file_async(str(main_file))
        else:
            messagebox.showerror("Error", "main.zpx not found in project root")
            
    def _toggle_console(self):
        pass
        
    def _toggle_params(self):
        pass
        
    def _reset_layout(self):
        pass
        
    def _open_docs(self):
        webbrowser.open("https://github.com/M-2000-0/ZAPphysics/blob/main/README.md")
        
    def _show_about(self):
        messagebox.showinfo("About ZapPhysics v4.2",
            "ZapPhysics v4.2 — Physics + Chemistry + Engineering + Aerospace\n\n"
            "22 Demos: N-body, Collision, Chemistry, EM, SPH, Rigid Body,\n"
            "Structural, Game, Broadphase, Rocket, Aero, Orbital, Flight.\n\n"
            "Language: Zap (custom Python-interpreted DSL)\n"
            "GUI: CustomTkinter + Matplotlib\n\n"
            "GitHub: https://github.com/M-2000-0/ZAPphysics")
            
    def _run_file_async(self, path: str):
        self.console.clear()
        self.console.write_system(f">>> Running: {os.path.basename(path)}\n\n")
        
        def run():
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = str(ZAP_SRC) + os.pathsep + os.environ.get('PYTHONPATH', '')
                
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
                
        threading.Thread(target=run, daemon=True).start()
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
                elif msg_type == "stderr":
                    self.console.write(content, "stderr")
                elif msg_type == "done":
                    self.running = False
                    self.controller.running = False
                    self.controller.play_btn.configure(text="▶")
                    return
        except queue.Empty:
            pass
        if self.running:
            self.after(50, self._process_sim_queue)


def main():
    """Application entry point."""
    # Setup logging
    import logging
    log_dir = Path.home() / ".zapphysics" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / f"zapphysics_{time.strftime('%Y%m%d')}.log", encoding='utf-8')
        ]
    )
    
    # Initialize core systems
    initialize_state()
    
    # Create and run app
    app = ZapPhysicsApp()
    app.mainloop()


if __name__ == "__main__":
    main()