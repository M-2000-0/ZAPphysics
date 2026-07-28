"""Parameter Panel with sliders and inputs for simulation parameters."""
import tkinter as tk
from tkinter import ttk
from gui.theme import *


class ParameterPanel(ttk.Frame):
    """Dynamic parameter panel that shows controls for the active simulation."""
    
    def __init__(self, parent, viz_canvas, zap_runner):
        super().__init__(parent)
        self.viz_canvas = viz_canvas
        self.zap_runner = zap_runner
        self.params = {}
        self.widgets = {}
        self._build_ui()

    def _build_ui(self):
        """Build parameter panel UI."""
        # Title
        ttk.Label(self, text="Simulation Parameters", style="Title.TLabel").pack(anchor=tk.W, padx=8, pady=8)
        
        # Scrollable container
        canvas = tk.Canvas(self, bg=PANEL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable = ttk.Frame(canvas)
        
        self.scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=8)
        
        # Mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta/120), "units"))

        # Preset selector
        self.preset_var = tk.StringVar(value="Custom")
        preset_frame = ttk.Frame(self.scrollable)
        preset_frame.pack(fill=tk.X, pady=4)
        ttk.Label(preset_frame, text="Preset:").pack(side=tk.LEFT, padx=4)
        ttk.Combobox(preset_frame, textvariable=self.preset_var, 
                    values=["Custom", "Orbital", "Rocket", "Flight", "Structural", "Chemistry"],
                    width=15, state="readonly").pack(side=tk.LEFT, padx=4)

        # Common simulation parameters
        self._add_param("dt", "Time Step (dt)", 0.001, 1.0, 0.01, 0.001)
        self._add_param("max_time", "Max Time (s)", 1.0, 1000.0, 10.0, 1.0)
        self._add_param("gravity", "Gravity", 0.0, 20.0, 9.81, 0.1)
        
        # Physics-specific params
        self._add_section("Orbital Mechanics")
        self._add_param("mu", "Gravitational Param (μ)", 1e10, 1e15, 3.986e14, 1e11)
        self._add_param("r1", "Initial Radius r1", 1e6, 1e11, 6.571e6, 1e6)
        self._add_param("r2", "Target Radius r2", 1e6, 1e11, 4.2157e7, 1e6)
        
        self._add_section("Rocket / Flight")
        self._add_param("mass", "Total Mass (kg)", 100, 1e6, 84000, 1000)
        self._add_param("thrust", "Thrust (N)", 1e4, 1e7, 8.45e5, 1e4)
        self._add_param("isp", "Specific Impulse (s)", 100, 500, 311, 1)
        self._add_param("propellant", "Propellant Mass (kg)", 100, 5e5, 40000, 1000)
        
        self._add_section("Structural")
        self._add_param("E", "Young's Modulus (Pa)", 1e9, 1e12, 2e11, 1e9)
        self._add_param("I", "Moment of Inertia", 1e-6, 1e-2, 8.33e-6, 1e-6)
        self._add_param("L", "Length (m)", 0.1, 100.0, 5.0, 0.1)
        self._add_param("load", "Load (N)", 100, 1e6, 10000, 100)

        self._add_section("Chemistry")
        self._add_param("k", "Rate Constant", 0.001, 10.0, 0.1, 0.001)
        self._add_param("order", "Reaction Order", 0, 3, 1, 1)
        self._add_param("A0", "Initial [A]", 0.01, 10.0, 1.0, 0.01)
        self._add_param("B0", "Initial [B]", 0.01, 10.0, 2.0, 0.01)

        # Apply button
        ttk.Button(self.scrollable, text="Apply to Visualization", 
                  command=self._apply_params, style="Accent.TButton").pack(pady=16, fill=tk.X, padx=8)

    def _add_section(self, title):
        """Add a section header."""
        sep = ttk.Separator(self.scrollable, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=8, padx=8)
        ttk.Label(self.scrollable, text=title, foreground=ACCENT, 
                 font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, padx=8)

    def _add_param(self, name, label, min_val, max_val, default, step):
        """Add a parameter slider/spinbox."""
        frame = ttk.Frame(self.scrollable)
        frame.pack(fill=tk.X, padx=8, pady=4)
        
        ttk.Label(frame, text=label, width=25).pack(side=tk.LEFT, padx=4)
        
        # Use appropriate widget based on value range
        if max_val - min_val > 100 and isinstance(default, float):
            # Slider for large ranges
            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(frame, from_=min_val, to=max_val, variable=var, 
                            orient=tk.HORIZONTAL, length=200)
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
            entry = ttk.Entry(frame, textvariable=var, width=12)
        else:
            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(frame, from_=min_val, to=max_val, variable=var, 
                            orient=tk.HORIZONTAL, length=200)
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
            entry = ttk.Entry(frame, textvariable=var, width=12)
        
        entry.pack(side=tk.LEFT, padx=4)
        
        self.params[name] = {"var": var, "min": min_val, "max": max_val, "step": step}
        self.widgets[name] = (scale, entry)

    def _apply_params(self):
        """Apply parameters to visualization."""
        values = {name: p["var"].get() for name, p in self.params.items()}
        self.viz_canvas.set_params(values)
        self._show_status("Parameters applied")

    def _show_status(self, msg):
        """Show temporary status message."""
        pass

    def get_params(self):
        """Get current parameter values."""
        return {name: p["var"].get() for name, p in self.params.items()}


class DemoBrowser(ttk.Frame):
    """Browser for built-in demos."""
    
    DEMOS = {
        "orbital": {"name": "Orbital Mechanics", "desc": "N-body orbital simulation", "file": "demo_orbital_mechanics.zap"},
        "rocket": {"name": "Rocket Engineering", "desc": "Multi-stage rocket design & flight", "file": "demo_rocket.zap"},
        "flight": {"name": "Flight Dynamics", "desc": "Aircraft flight envelope & simulation", "file": "demo_flight.zap"},
        "structural": {"name": "Structural Analysis", "desc": "Truss & beam analysis", "file": "demo_structural.zap"},
        "chemistry": {"name": "Chemistry Lab", "desc": "Molecules, reactions, thermodynamics", "file": "demo_chemistry.zap"},
        "kinetics": {"name": "Reaction Kinetics", "desc": "Rate laws, equilibrium, enzyme kinetics", "file": "demo_kinetics.zap"},
        "rigid": {"name": "Rigid Body", "desc": "Rotation, torque, inertia", "file": "demo_rigid.zap"},
        "collision": {"name": "Elastic Collisions", "desc": "2D particle collisions", "file": "collisions.zap"},
        "springs": {"name": "Spring-Mass System", "desc": "Oscillations & energy", "file": "springs.zap"},
        "em": {"name": "Electromagnetics", "desc": "Coulomb, Lorentz, fields", "file": "demo_em.zap"},
        "fluid": {"name": "SPH Fluid", "desc": "Smoothed particle hydrodynamics", "file": "demo_fluid.zap"},
        "3d": {"name": "3D Particles", "desc": "3D orbital simulation", "file": "demo3d.zap"},
        "elements": {"name": "Periodic Table", "desc": "118 elements", "file": "demo_elements.zap"},
        "game": {"name": "Game Physics", "desc": "Platformer, top-down, ragdoll", "file": "demo_game.zap"},
        "art": {"name": "Generative Art", "desc": "Particle art & visualization", "file": "demo_art.zap"},
        "visual": {"name": "ASCII Visualization", "desc": "Charts, heatmaps, sparklines", "file": "demo_visual.zap"},
        "tensor": {"name": "Tensor N-Body", "desc": "Matrix-based force calc", "file": "tensor.zap"},
        "orbital3d": {"name": "3D Orbital (Velocity Verlet)", "desc": "3D N-body with VV integrator", "file": "demo_orbital3d.zap"},
        "lambert": {"name": "Lambert Solver", "desc": "Orbital targeting & rendezvous", "file": "demo_lambert.zap"},
        "porkchop": {"name": "Porkchop Plot", "desc": "Launch window analysis", "file": "demo_porkchop.zap"},
        "broadphase": {"name": "Broad-phase Collision", "desc": "Grid & quadtree acceleration", "file": "demo_broadphase.zap"},
        "constraints": {"name": "Constraint System", "desc": "Distance, spring, hinge, slider", "file": "demo_constraints.zap"},
    }

    def __init__(self, parent, script_editor, zap_runner):
        super().__init__(parent)
        self.script_editor = script_editor
        self.zap_runner = zap_runner
        self.current_demo = None
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Built-in Demos", style="Title.TLabel").pack(anchor=tk.W, padx=8, pady=8)
        
        # Search
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=8, pady=4)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_demos)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(fill=tk.X)
        
        # Demo list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        self.demo_list = tk.Listbox(list_frame, bg=PANEL, fg=FG, font=("Segoe UI", 9),
                                   selectbackground=ACCENT, borderwidth=0, highlightthickness=0)
        self.demo_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.demo_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.demo_list.configure(yscrollcommand=scroll.set)
        
        self.demo_list.bind("<Double-Button-1>", self._on_select)
        self.demo_list.bind("<Return>", self._on_select)
        
        self._populate_list()

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(btn_frame, text="Load Demo", command=self._on_select, style="Accent.TButton").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(btn_frame, text="Run", command=self._run_demo).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(btn_frame, text="View Source", command=self._view_source).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def _populate_list(self):
        self.demo_list.delete(0, tk.END)
        for key, demo in self.DEMOS.items():
            self.demo_list.insert(tk.END, f"{demo['name']}  —  {demo['desc']}")

    def _filter_demos(self, *args):
        query = self.search_var.get().lower()
        self.demo_list.delete(0, tk.END)
        for key, demo in self.DEMOS.items():
            if query in demo['name'].lower() or query in demo['desc'].lower():
                self.demo_list.insert(tk.END, f"{demo['name']}  —  {demo['desc']}")

    def _on_select(self, event=None):
        sel = self.demo_list.curselection()
        if not sel:
            return
        idx = sel[0]
        keys = list(self.DEMOS.keys())
        if idx < len(keys):
            self.load_demo(keys[idx])

    def load_demo(self, demo_key):
        """Load a demo into the script editor."""
        import os
        demo = self.DEMOS.get(demo_key)
        if not demo:
            return
        
        examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")
        filepath = os.path.join(examples_dir, demo['file'])
        
        if os.path.exists(filepath):
            self.script_editor.load_file(filepath)
            self.current_demo = demo_key
        else:
            # Try loading from lib
            lib_dir = os.path.join(os.path.dirname(__file__), "..", "..", "lib")
            filepath = os.path.join(lib_dir, demo['file'])
            if os.path.exists(filepath):
                self.script_editor.load_file(filepath)
                self.current_demo = demo_key

    def _run_demo(self):
        if self.current_demo:
            self.script_editor.master.master._run_script()

    def _view_source(self):
        if self.current_demo:
            demo = self.DEMOS[self.current_demo]
            import os
            examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")
            filepath = os.path.join(examples_dir, demo['file'])
            if os.path.exists(filepath):
                self.script_editor.load_file(filepath)

    def get_demo_names(self):
        return [d['name'] for d in self.DEMOS.values()]