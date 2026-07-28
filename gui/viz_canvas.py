"""Visualization Canvas with real-time matplotlib rendering."""
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from gui.theme import *


class VizCanvas(ttk.Frame):
    """Interactive matplotlib visualization canvas."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.current_figure = None
        self.canvas = None
        self.toolbar = None
        self.params = {}
        self._build_ui()
        
    def _build_ui(self):
        """Build visualization UI."""
        # Toolbar frame
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(fill=tk.X, padx=4, pady=4)
        
        ttk.Label(toolbar_frame, text="Visualization", style="Title.TLabel").pack(side=tk.LEFT)
        
        # Plot type selector
        self.plot_type = tk.StringVar(value="particles")
        ttk.Combobox(toolbar_frame, textvariable=self.plot_type, width=15,
                    values=["particles", "trajectories", "energy", "fields", "3d"],
                    state="readonly").pack(side=tk.RIGHT, padx=4)
        ttk.Label(toolbar_frame, text="Plot:").pack(side=tk.RIGHT, padx=4)
        
        # Clear/Export buttons
        ttk.Button(toolbar_frame, text="Clear", command=self.clear, width=8).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar_frame, text="Export PNG", command=self.export_image, width=10).pack(side=tk.RIGHT, padx=2)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor=BG)
        self.ax = self.figure.add_subplot(111)
        self._style_axes()
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.canvas.mpl_connect('scroll_event', self._on_scroll)
        self.canvas.mpl_connect('button_press_event', self._on_click)
        
        # Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(fill=tk.X, padx=4, pady=4)
        
        # Initial plot
        self._draw_placeholder()
        
    def _style_axes(self):
        """Apply dark theme to matplotlib axes."""
        self.ax.set_facecolor(PANEL)
        self.ax.tick_params(colors=FG, which='both')
        self.ax.spines['bottom'].set_color(BORDER)
        self.ax.spines['top'].set_color(BORDER)
        self.ax.spines['left'].set_color(BORDER)
        self.ax.spines['right'].set_color(BORDER)
        self.ax.xaxis.label.set_color(FG)
        self.ax.yaxis.label.set_color(FG)
        self.ax.title.set_color(ACCENT)
        self.figure.set_facecolor(BG)
        
    def _draw_placeholder(self):
        """Draw initial placeholder."""
        self.ax.clear()
        self._style_axes()
        self.ax.text(0.5, 0.5, "Run a simulation to visualize", 
                    ha='center', va='center', color=FG_DIM, fontsize=14,
                    transform=self.ax.transAxes)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
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
            self.figure.savefig(path, dpi=300, facecolor=BG, edgecolor='none')
            
    def _on_scroll(self, event):
        """Handle mouse scroll for zoom."""
        if event.inaxes:
            scale = 1.1 if event.button == 'up' else 0.9
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            xdata, ydata = event.xdata, event.ydata
            self.ax.set_xlim([xdata - (xdata - xlim[0]) * scale,
                             xdata + (xlim[1] - xdata) * scale])
            self.ax.set_ylim([ydata - (ydata - ylim[0]) * scale,
                             ydata + (ylim[1] - ydata) * scale])
            self.canvas.draw()
            
    def _on_click(self, event):
        """Handle mouse click."""
        pass
        
    def plot_particles(self, positions, colors=None, sizes=None, trails=None):
        """Plot particle positions."""
        self.ax.clear()
        self._style_axes()
        
        positions = np.array(positions)
        if len(positions) == 0:
            self._draw_placeholder()
            return
            
        if colors is None:
            colors = [ACCENT] * len(positions)
        if sizes is None:
            sizes = [50] * len(positions)
            
        self.ax.scatter(positions[:, 0], positions[:, 1], c=colors, s=sizes, alpha=0.8)
        
        if trails is not None:
            for trail in trails:
                trail = np.array(trail)
                if len(trail) > 1:
                    self.ax.plot(trail[:, 0], trail[:, 1], '-', alpha=0.3, color=ACCENT, linewidth=1)
                    
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
                color = labels[i] if labels and i < len(labels) else plt.cm.tab10(i % 10)
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
        
        self.ax.quiver(X, Y, U, V, color=ACCENT, alpha=0.7)
        self.ax.set_title(title)
        self.ax.set_aspect('equal')
        self.canvas.draw()
        
    def plot_3d(self, positions, colors=None):
        """3D scatter plot."""
        if not hasattr(self, 'ax3d'):
            self.figure.clear()
            self.ax3d = self.figure.add_subplot(111, projection='3d')
            self._style_axes_3d()
        else:
            self.ax3d.clear()
            self._style_axes_3d()
            
        positions = np.array(positions)
        if colors is None:
            colors = [ACCENT] * len(positions)
            
        self.ax3d.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                         c=colors, s=30, alpha=0.8)
        self.ax3d.set_xlabel('X')
        self.ax3d.set_ylabel('Y')
        self.ax3d.set_zlabel('Z')
        self.canvas.draw()
        
    def _style_axes_3d(self):
        """Style 3D axes."""
        self.ax3d.set_facecolor(PANEL)
        for axis in [self.ax3d.xaxis, self.ax3d.yaxis, self.ax3d.zaxis]:
            axis.set_tick_params(colors=FG)
            axis.label.set_color(FG)
            axis._axinfo['grid']['color'] = BORDER
        self.ax3d.title.set_color(ACCENT)
        
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


class SimController(ttk.Frame):
    """Simulation control bar with play/pause/step/speed controls."""
    
    def __init__(self, parent, app_ref):
        super().__init__(parent)
        self.app = app_ref
        self.running = False
        self.speed = 1.0
        self._build_ui()
        
    def _build_ui(self):
        """Build controller UI."""
        # Play/Pause/Stop
        ttk.Button(self, text="⏮", command=self.app._restart_sim, width=3).pack(side=tk.LEFT, padx=2)
        self.play_btn = ttk.Button(self, text="▶", command=self._toggle_play, width=3, style="Accent.TButton")
        self.play_btn.pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="⏸", command=self.app._stop_sim, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="⏭", command=self._step_frame, width=3).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        
        # Speed control
        ttk.Label(self, text="Speed:").pack(side=tk.LEFT, padx=4)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(self, from_=0.1, to=10.0, variable=self.speed_var,
                               orient=tk.HORIZONTAL, length=120,
                               command=self._on_speed_change)
        speed_scale.pack(side=tk.LEFT, padx=4)
        ttk.Label(self, textvariable=tk.StringVar(value="1.0x")).pack(side=tk.LEFT)
        
        # Frame counter
        self.frame_var = tk.StringVar(value="Frame: 0 / 0")
        ttk.Label(self, textvariable=self.frame_var, foreground=INFO).pack(side=tk.LEFT, padx=16)
        
        # Time display
        self.time_var = tk.StringVar(value="Time: 0.00s")
        ttk.Label(self, textvariable=self.time_var, foreground=FG_DIM).pack(side=tk.LEFT, padx=8)
        
    def _toggle_play(self):
        """Toggle play/pause."""
        if self.running:
            self.running = False
            self.play_btn.config(text="▶")
        else:
            self.running = True
            self.play_btn.config(text="⏸")
            self.app._run_script()
            
    def _step_frame(self):
        """Step one frame."""
        pass
        
    def _on_speed_change(self, val):
        """Handle speed change."""
        self.speed = float(val)
        
    def update_state(self):
        """Update controller display."""
        if hasattr(self.app, 'sim_thread') and self.app.sim_thread and self.app.sim_thread.is_alive():
            if not self.running:
                self.running = True
                self.play_btn.config(text="⏸")
        else:
            if self.running:
                self.running = False
                self.play_btn.config(text="▶")