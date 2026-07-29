"""
ZapPhysics Professional — Visualization Canvas
Real-time matplotlib visualization with multiple plot types.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from typing import Dict, Any, List, Optional, Tuple


# Colors
COLORS = {
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#1f2428",
    "border_default": "#30363d",
    "accent_primary": "#58a6ff",
    "accent_hover": "#79b8ff",
    "fg_primary": "#e6edf3",
    "fg_secondary": "#8b949e",
    "fg_muted": "#6e7681",
}


class VizCanvas(ctk.CTkFrame):
    """Professional visualization canvas with Matplotlib."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#0d1117", corner_radius=8, border_width=1, border_color="#30363d", **kwargs)
        self.params: Dict[str, Any] = {}
        self.plot_type = ctk.StringVar(value="particles")
        self._build_ui()
        
    def _build_ui(self):
        """Build visualization UI."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent", height=40)
        toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        toolbar.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(toolbar, text="Visualization", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=8)
        
        # Plot type selector
        ctk.CTkLabel(toolbar, text="Plot:").pack(side="right", padx=8)
        ctk.CTkComboBox(
            toolbar, values=["particles", "trajectories", "energy", "fields", "3d"],
            variable=self.plot_type, width=120
        ).pack(side="right", padx=8)
        
        # Clear/Export buttons
        from .widgets import ProButton
        ProButton(self, text="Clear", variant="ghost", width=70, command=self.clear).place(relx=0.9, rely=0.5, anchor="e")
        ProButton(self, text="Export", variant="ghost", width=70, command=self.export_image).place(relx=0.82, rely=0.5, anchor="e")
        
        # Matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor="#0d1117")
        self.ax = self.fig.add_subplot(111)
        self._style_axes()
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        
        # Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.toolbar.config(background="#0d1117")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._draw_placeholder()
        
    def _style_axes(self):
        """Apply dark theme to matplotlib axes."""
        self.ax.set_facecolor("#161b22")
        self.ax.tick_params(colors="#e6edf3", which='both')
        for spine in self.ax.spines.values():
            spine.set_color("#30363d")
        self.ax.xaxis.label.set_color("#e6edf3")
        self.ax.yaxis.label.set_color("#e6edf3")
        self.ax.title.set_color("#58a6ff")
        self.fig.set_facecolor("#0d1117")
        
    def _draw_placeholder(self):
        """Draw initial placeholder."""
        self.ax.clear()
        self._style_axes()
        self.ax.text(0.5, 0.5, "Run a simulation to visualize", 
                    ha='center', va='center', color="#6e7681", fontsize=14,
                    transform=self.ax.transAxes)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
        
    def set_params(self, params: dict):
        """Update visualization parameters."""
        self.params = params
        
    def clear(self):
        """Clear the visualization."""
        self.ax.clear()
        self._style_axes()
        self._draw_placeholder()
        
    def export_image(self):
        """Export current figure as PNG."""
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")],
            title="Export Visualization"
        )
        if path:
            self.fig.savefig(path, dpi=300, facecolor="#0d1117", edgecolor='none')
            
    def plot_particles(self, positions, colors=None, sizes=None, trails=None):
        """Plot particle positions."""
        self.ax.clear()
        self._style_axes()
        
        positions = np.array(positions)
        if len(positions) == 0:
            self._draw_placeholder()
            return
            
        if colors is None:
            colors = ["#58a6ff"] * len(positions)
        if sizes is None:
            sizes = [50] * len(positions)
            
        self.ax.scatter(positions[:, 0], positions[:, 1], c=colors, s=sizes, alpha=0.8)
        
        if trails is not None:
            for trail in trails:
                trail = np.array(trail)
                if len(trail) > 1:
                    self.ax.plot(trail[:, 0], trail[:, 1], '-', color="#58a6ff", alpha=0.3, linewidth=1)
                    
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.margins(0.1)
        self.canvas.draw()
        
    def plot_trajectories(self, trajectories, labels=None):
        """Plot multiple trajectories."""
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
        self.canvas.draw()
        
    def plot_energy(self, time, energies, labels=None):
        """Plot energy vs time."""
        self.ax.clear()
        self._style_axes()
        
        for i, energy in enumerate(energies):
            label = labels[i] if labels and i < len(labels) else f"Energy {i+1}"
            self.ax.plot(time, energy, '-', label=label, linewidth=1.5)
            
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Energy (J)")
        self.ax.legend(loc='upper right', fontsize=8)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        
    def plot_field(self, X, Y, U, V, title="Vector Field"):
        """Plot 2D vector field."""
        self.ax.clear()
        self._style_axes()
        
        self.ax.quiver(X, Y, U, V, color="#58a6ff", alpha=0.7)
        self.ax.set_title(title)
        self.ax.set_aspect('equal')
        self.canvas.draw()
        
    def plot_3d(self, positions, colors=None):
        """3D scatter plot."""
        if not hasattr(self, 'ax3d'):
            self.fig.clear()
            self.ax3d = self.fig.add_subplot(111, projection='3d')
            self._style_axes_3d()
        else:
            self.ax3d.clear()
            self._style_axes_3d()
            
        positions = np.array(positions)
        if colors is None:
            colors = ["#58a6ff"] * len(positions)
            
        self.ax3d.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                         c=colors, s=30, alpha=0.8)
        self.ax3d.set_xlabel('X')
        self.ax3d.set_ylabel('Y')
        self.ax3d.set_zlabel('Z')
        self.canvas.draw()
        
    def _style_axes_3d(self):
        """Style 3D axes."""
        self.ax3d.set_facecolor("#161b22")
        for axis in [self.ax3d.xaxis, self.ax3d.yaxis, self.ax3d.zaxis]:
            axis.set_tick_params(colors="#e6edf3")
            axis.label.set_color("#e6edf3")
            axis._axinfo['grid']['color'] = "#30363d"
        self.ax3d.title.set_color("#58a6ff")
        self.fig.set_facecolor("#0d1117")
        
    def update_from_simulation(self, sim_data: dict):
        """Update visualization from simulation data."""
        plot_type = self.plot_type.get()
        
        if plot_type == "particles" and "positions" in sim_data:
            self.plot_particles(sim_data["positions"], 
                              sim_data.get("colors"), 
                              sim_data.get("sizes"),
                              sim_data.get("trails"))
        elif plot_type == "trajectories" and "trajectories" in sim_data:
            self.plot_trajectories(sim_data["trajectories"], sim_data.get("labels"))
        elif plot_type == "energy" and "time" in sim_data and "energies" in sim_data:
            self.plot_energy(sim_data["time"], sim_data["energies"], sim_data.get("labels"))
        elif plot_type == "3d" and "positions" in sim_data:
            self.plot_3d(sim_data["positions"], sim_data.get("colors"))
            
    def update_params(self, params):
        """Update visualization parameters."""
        self.params.update(params)


class SimController(ctk.CTkFrame):
    """Simulation control bar with play/pause/step/speed controls."""
    
    def __init__(self, master, app_ref, **kwargs):
        super().__init__(master, fg_color="#161b22", corner_radius=10, border_width=1, border_color="#30363d", height=60, **kwargs)
        self.app = app_ref
        self.running = False
        self.speed = 1.0
        self._build_ui()
        
    def _build_ui(self):
        """Build controller UI."""
        self.pack_propagate(False)
        self.grid_columnconfigure(4, weight=1)
        
        # Restart
        from .widgets import ProButton
        ProButton(self, text="⏮", width=44, height=36, variant="secondary", command=self.app.restart_sim).pack(side="left", padx=8, pady=12)
        
        # Play/Pause
        self.play_btn = ProButton(self, text="▶", width=44, height=36, variant="primary", command=self._toggle)
        self.play_btn.pack(side="left", padx=4, pady=12)
        
        # Stop
        ProButton(self, text="■", width=44, height=36, variant="secondary", command=self.app.stop_sim).pack(side="left", padx=4, pady=12)
        
        # Step
        ProButton(self, text="⏭", width=44, height=36, variant="secondary", command=self._step).pack(side="left", padx=4, pady=12)
        
        # Separator
        ctk.CTkFrame(self, width=1, fg_color="#30363d").pack(side="left", fill="y", padx=12, pady=8)
        
        # Speed control
        ctk.CTkLabel(self, text="Speed:", font=ctk.CTkFont(size=12)).pack(side="left", padx=4)
        self.speed_var = ctk.DoubleVar(value=1.0)
        speed_scale = ctk.CTkSlider(self, from_=0.1, to=10.0, variable=self.speed_var,
                                  width=120,
                                  command=self._on_speed)
        speed_scale.pack(side="left", padx=4)
        self.speed_label = ctk.CTkLabel(self, text="1.0×", width=40, font=ctk.CTkFont(weight="bold"))
        self.speed_label.pack(side="left", padx=4)
        
        # Frame counter
        self.frame_var = ctk.StringVar(value="Frame: 0 / 0")
        ctk.CTkLabel(self, textvariable=self.frame_var, text_color="#58a6ff", 
                    font=ctk.CTkFont(weight="bold")).pack(side="left", padx=16)
        
        # Time display
        self.time_var = ctk.StringVar(value="Time: 0.00s")
        ctk.CTkLabel(self, textvariable=self.time_var, text_color="#8b949e").pack(side="left", padx=8)
        
    def _toggle(self):
        """Toggle play/pause."""
        if self.running:
            self.running = False
            self.play_btn.configure(text="▶")
        else:
            self.running = True
            self.play_btn.configure(text="⏸")
            self.app.run_current()
            
    def _step(self):
        """Step one frame."""
        pass
        
    def _on_speed(self, val):
        """Handle speed change."""
        self.speed = float(val)
        self.speed_label.configure(text=f"{self.speed:.1f}×")
        
    def update_state(self):
        """Update controller display."""
        if hasattr(self.app, 'sim_thread') and self.app.sim_thread and self.app.sim_thread.is_alive():
            if not self.running:
                self.running = True
                self.play_btn.configure(text="⏸")
        else:
            if self.running:
                self.running = False
                self.play_btn.configure(text="▶")


class DemoBrowser(ctk.CTkFrame):
    """Built-in demo browser and quick-launch panel."""
    
    DEMOS = {
        "orbital": ("Orbital Mechanics", "examples/demo_orbital.zap", "N-body orbital simulation with Hohmann transfers"),
        "orbital3d": ("3D Orbital (VV)", "examples/demo_orbital3d.zap", "3D velocity verlet integration"),
        "lambert": ("Lambert Solver", "examples/demo_lambert.zap", "Orbital targeting & rendezvous"),
        "porkchop": ("Porkchop Plot", "examples/demo_porkchop.zap", "Launch window analysis Earth→Mars"),
        "rocket": ("Rocket Engineering", "examples/demo_rocket.zap", "Multi-stage rocket design & trajectory"),
        "flight": ("Flight Dynamics", "examples/demo_flight.zap", "Aircraft aerodynamics & envelope"),
        "structural": ("Structural Eng", "examples/demo_structural.zap", "Truss & beam analysis"),
        "game": ("Game Physics", "examples/demo_game.zap", "Platformer, top-down, ragdoll"),
        "collisions": ("Collisions", "examples/collisions.zap", "Elastic collision dynamics"),
        "springs": ("Spring-Mass", "examples/springs.zap", "Oscillator systems"),
        "chemistry": ("Chemistry Lab", "examples/chemistry.zap", "Molecules, reactions, thermodynamics"),
        "elements": ("Periodic Table", "examples/demo_elements.zap", "118 elements"),
        "kinetics": ("Reaction Kinetics", "examples/demo_kinetics.zap", "Rate laws, equilibrium, enzymes"),
        "em": ("Electromagnetics", "examples/demo_em.zap", "Coulomb, Lorentz, fields"),
        "fluid": ("SPH Fluids", "examples/demo_fluid.zap", "Smoothed particle hydrodynamics"),
        "rigid": ("Rigid Body", "examples/demo_rigid.zap", "Rotation, torque, inertia"),
        "tensor": ("Tensor N-Body", "examples/tensor.zap", "Matrix force calculations"),
        "visual": ("ASCII Viz", "examples/demo_visual.zap", "Charts, sparklines, heatmaps"),
        "art": ("Generative Art", "examples/demo_art.zap", "Particle fountains, spirals, bursts"),
        "broadphase": ("Broadphase", "examples/demo_broadphase.zap", "Grid & quadtree collision"),
        "constraints": ("Constraints", "examples/demo_constraints.zap", "Distance, spring, hinge, slider"),
    }
    
    def __init__(self, master, on_load, on_run, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_load = on_load
        self.on_run = on_run
        self._build_ui()
        
    def _build_ui(self):
        """Build demo browser UI."""
        # Search/filter
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=4, pady=4)
        
        ctk.CTkLabel(search_frame, text="🔍").pack(side="left", padx=2)
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter_demos)
        ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search...", 
                    height=32).pack(side="left", fill="x", expand=True, padx=4)
        
        # Demo list
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Treeview for demo list
        columns = ("desc",)
        self.tree = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.tree.pack(fill="both", expand=True, padx=4, pady=4)
        
        self.cards = {}
        for key, (name, path, desc) in self.DEMOS.items():
            self._add_card(key, name, desc)
            
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=4, pady=4)
        
        ctk.CTkButton(btn_frame, text="Load", command=self._load_selected, 
                     fg_color="#58a6ff", hover_color="#79b8ff", height=36).pack(side="left", padx=2, fill="x", expand=True)
        ctk.CTkButton(btn_frame, text="Run", fg_color="#3fb950", hover_color="#4ac45a",
                     command=self._run_selected, height=36).pack(side="left", padx=2, fill="x", expand=True)

    def _add_card(self, key, name, path, desc):
        card = ctk.CTkFrame(self.tree, fg_color="#1f2428", corner_radius=8, border_width=1, border_color="#30363d")
        card.pack(fill="x", pady=4, padx=4)
        card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(weight="bold", size=13)).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(card, text=desc, text_color="#8b949e", font=ctk.CTkFont(size=11), wraplength=240).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        
        card.bind("<Button-1>", lambda e, k=key: self._select(k))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, k=key: self._select(k))
        
        self.demo_cards[key] = card

    def _filter_demos(self, *args):
        query = self.search_var.get().lower()
        for key, (name, _, desc) in self.DEMOS.items():
            match = query in name.lower() or query in desc.lower()
            # Visibility logic would go here

    def _select(self, key):
        for k, card in self.demo_cards.items():
            card.configure(border_color="#58a6ff" if k == key else "#30363d")
        self.selected_key = key

    def _load_selected(self):
        if hasattr(self, 'selected_key'):
            self.on_load(self.selected_key)

    def _run_selected(self):
        if hasattr(self, 'selected_key'):
            self.on_run(self.selected_key)

    def get_demo_names(self):
        return [info[0].lower().replace(" ", "_") for info in self.DEMOS.values()]

    def load_demo(self, name):
        for key, (disp_name, path, _) in self.DEMOS.items():
            if disp_name.lower().replace(" ", "_") == name.lower():
                self.on_load(key)
                break