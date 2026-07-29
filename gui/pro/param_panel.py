"""
ZapPhysics Professional — Parameter Panel
Dynamic parameter controls for simulation configuration.
"""

import customtkinter as ctk
from typing import Dict, Any, List, Optional, Callable


class ParameterPanel(ctk.CTkFrame):
    """Dynamic parameter panel with sliders, entries, and presets."""
    
    def __init__(self, master, on_apply: Callable = None, **kwargs):
        super().__init__(master, fg_color="#161b22", corner_radius=8, border_width=1, border_color="#30363d", **kwargs)
        self.on_apply = on_apply
        self.params: Dict[str, Dict[str, Any]] = {}
        self.widgets: Dict[str, Any] = {}
        self._build_ui()
        
    def _build_ui(self):
        """Build the parameter panel UI."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=36)
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=4)
        ctk.CTkLabel(header, text="Parameters", font=ctk.CTkFont(weight="bold", size=13)).pack(side="left")
        ctk.CTkLabel(header, text=f"0 controls", text_color="#8b949e", font=ctk.CTkFont(size=11)).pack(side="right")
        
        # Scrollable content
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        self.scroll.grid_columnconfigure(0, weight=1)
        
        # Bottom bar
        bottom = ctk.CTkFrame(self, fg_color="transparent", height=40)
        bottom.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))
        bottom.grid_columnconfigure(0, weight=1)
        
        from .widgets import ProButton
        self.apply_btn = ProButton(bottom, text="Apply", variant="primary", height=32, command=self._apply)
        self.apply_btn.grid(row=0, column=0, padx=4, sticky="ew")
        ProButton(bottom, text="Reset", variant="ghost", height=32, command=self._reset).grid(row=0, column=1, padx=4)
        
        self._add_presets()
        self._add_common_params()
        
    def _add_presets(self):
        """Add preset selector."""
        frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="ew", pady=4, padx=4)
        frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame, text="Preset:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=(0, 8))
        self.preset_var = ctk.StringVar(value="Custom")
        preset_combo = ctk.CTkComboBox(
            frame, values=["Custom", "Orbital", "Rocket", "Flight", "Structural", "Chemistry"],
            variable=self.preset_var, width=180, height=28, command=self._on_preset
        )
        preset_combo.grid(row=0, column=1, sticky="ew")
        
        ctk.CTkFrame(self.scroll, height=1, fg_color="#30363d").grid(row=1, column=0, sticky="ew", pady=4)
        
    def _add_common_params(self):
        """Add common simulation parameters."""
        row = 2
        
        # Section header
        self._add_section(row, "Simulation")
        row += 1
        
        row = self._add_slider(row, "dt", "Time Step", 0.001, 1.0, 0.01, "s")
        row = self._add_slider(row, "max_time", "Max Time", 1.0, 1000.0, 10.0, "s")
        row = self._add_slider(row, "gravity", "Gravity", 0.0, 20.0, 9.81, "m/s²")
        
        # Section: Orbital
        self._add_section(row, "Orbital Mechanics")
        row += 1
        row = self._add_slider(row, "mu", "Gravitational μ", 1e10, 1e15, 3.986e14, "m³/s²")
        row = self._add_slider(row, "r1", "Initial Radius", 1e6, 1e11, 6.571e6, "m")
        row = self._add_slider(row, "r2", "Target Radius", 1e6, 1e11, 4.2157e7, "m")
        
        # Section: Rocket
        self._add_section(row, "Rocket / Flight")
        row += 1
        row = self._add_slider(row, "mass", "Total Mass", 100, 1e6, 84000, "kg")
        row = self._add_slider(row, "thrust", "Thrust", 1e4, 1e7, 8.45e5, "N")
        row = self._add_slider(row, "isp", "Specific Impulse", 100, 500, 311, "s")
        
        # Section: Structural
        self._add_section(row, "Structural")
        row += 1
        row = self._add_slider(row, "E", "Young's Modulus", 1e9, 1e12, 2e11, "Pa")
        row = self._add_slider(row, "L", "Length", 0.1, 100.0, 5.0, "m")
        
        # Section: Chemistry
        self._add_section(row, "Chemistry")
        row += 1
        row = self._add_slider(row, "k", "Rate Constant", 0.001, 10.0, 0.1, "1/s")
        row = self._add_slider(row, "A0", "Initial [A]", 0.01, 10.0, 1.0, "M")
        
        self.total_rows = row
        
    def _add_section(self, row: int, title: str):
        """Add a section divider with title."""
        frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", pady=(8, 2), padx=4)
        
        ctk.CTkLabel(frame, text=title.upper(), font=ctk.CTkFont(size=10, weight="bold"),
                    text_color="#58a6ff").pack(side="left", padx=4)
        ctk.CTkFrame(frame, height=1, fg_color="#30363d").pack(side="left", fill="x", expand=True, padx=8)
        
    def _add_slider(self, row: int, name: str, label: str, min_val: float, max_val: float, default: float, unit: str = "") -> int:
        """Add a parameter slider."""
        frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", pady=2, padx=4)
        frame.grid_columnconfigure(2, weight=1)
        
        # Label
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11), width=100, anchor="w").grid(row=0, column=0, padx=(4, 4))
        
        # Value display
        var = ctk.DoubleVar(value=default)
        val_label = ctk.CTkLabel(frame, text=f"{default:.4g}", font=ctk.CTkFont(size=10, weight="bold"),
                                text_color="#58a6ff", width=60, anchor="e")
        val_label.grid(row=0, column=1, padx=(0, 4))
        
        # Slider
        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=var,
                             command=lambda v, n=name, vl=val_label, u=unit: self._on_slide(v, n, vl, u))
        slider.grid(row=0, column=2, sticky="ew", padx=4)
        
        # Min/Max labels
        ctk.CTkLabel(frame, text=f"{min_val:.1g}", font=ctk.CTkFont(size=9), text_color="#6e7681").grid(row=1, column=2, sticky="w", padx=4)
        ctk.CTkLabel(frame, text=f"{max_val:.1g}", font=ctk.CTkFont(size=9), text_color="#6e7681").grid(row=1, column=2, sticky="e", padx=4)
        
        self.params[name] = {"var": var, "min": min_val, "max": max_val, "default": default, "slider": slider, "label": val_label, "unit": unit}
        
        return row + 1
        
    def _on_slide(self, val, name: str, label, unit: str):
        """Handle slider value change."""
        v = float(val)
        label.configure(text=f"{v:.4g}{' ' + unit if unit else ''}")
        
    def _apply(self):
        """Apply current parameters."""
        values = {name: p["var"].get() for name, p in self.params.items()}
        if self.on_apply:
            self.on_apply(values)
            
    def _reset(self):
        """Reset all parameters to defaults."""
        for name, p in self.params.items():
            p["var"].set(p["default"])
            self._on_slide(p["default"], name, p["label"], p.get("unit", ""))
            
    def _on_preset(self, choice: str):
        """Handle preset selection."""
        presets = {
            "Orbital": {"dt": 0.1, "max_time": 100, "gravity": 0, "mu": 3.986e14, "r1": 6.571e6, "r2": 4.2157e7},
            "Rocket": {"dt": 0.5, "max_time": 500, "gravity": 9.81, "mass": 84000, "thrust": 8.45e5, "isp": 311},
            "Flight": {"dt": 0.05, "max_time": 60, "gravity": 9.81, "mass": 50000, "thrust": 2e5},
            "Structural": {"dt": 0.01, "max_time": 10, "E": 2e11, "L": 5.0},
            "Chemistry": {"dt": 0.1, "max_time": 50, "k": 0.1, "A0": 1.0},
        }
        preset = presets.get(choice, {})
        for name, val in preset.items():
            if name in self.params:
                self.params[name]["var"].set(val)
                self._on_slide(val, name, self.params[name]["label"], self.params[name].get("unit", ""))
                
    def get_params(self) -> dict:
        """Get current parameter values."""
        return {name: p["var"].get() for name, p in self.params.items()}
        
    def set_params(self, params: dict):
        """Set parameter values programmatically."""
        for name, val in params.items():
            if name in self.params:
                self.params[name]["var"].set(val)
                self._on_slide(val, name, self.params[name]["label"], self.params[name].get("unit", ""))
                
    def clear(self):
        """Clear all parameters."""
        for name, p in self.params.items():
            p["var"].set(p["default"])
            self._on_slide(p["default"], name, p["label"], p.get("unit", ""))