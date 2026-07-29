"""
ZapPhysics Professional — Core Widgets
Reusable UI components with consistent styling.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Any, Callable, Dict, List, Optional, Tuple
from pathlib import Path
import re


# Color palette (imported from theme in practice)
COLORS = {
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#1f2428",
    "bg_hover": "#1f2428",
    "bg_active": "#263037",
    "fg_primary": "#e6edf3",
    "fg_secondary": "#8b949e",
    "fg_muted": "#6e7681",
    "fg_disabled": "#484f58",
    "accent_primary": "#58a6ff",
    "accent_hover": "#79b8ff",
    "accent_dim": "#1f6feb",
    "accent_fg": "#ffffff",
    "success": "#3fb950",
    "success_hover": "#4ac45a",
    "warning": "#d29922",
    "warning_hover": "#e3b341",
    "error": "#f85149",
    "error_hover": "#ff7b72",
    "border_default": "#30363d",
    "border_muted": "#21262d",
    "border_focus": "#58a6ff",
    "selection_bg": "#264f78",
    "selection_fg": "#ffffff",
    "code_bg": "#0d1117",
    "line_num_bg": "#161b22",
    "line_num_fg": "#484f58",
    "current_line_bg": "#1e2a38",
    "selection_bg_editor": "#264f78",
    "code_bg": "#0d1117",
    "selection_bg_editor": "#264f78",
    "console_bg": "#0d1117",
}


# ════════════════════════════════════════════════════════════════════
# Base Widgets
# ════════════════════════════════════════════════════════════════════

class ProFrame(ctk.CTkFrame):
    """Professional frame with consistent styling."""
    def __init__(self, master, variant: str = "default", **kwargs):
        variants = {
            "default": {"fg_color": COLORS["bg_secondary"], "border_color": COLORS["border_default"], "border_width": 1},
            "card": {"fg_color": COLORS["bg_tertiary"], "border_color": COLORS["border_default"], "border_width": 1},
            "panel": {"fg_color": COLORS["bg_primary"], "border_color": COLORS["border_default"], "border_width": 1},
            "transparent": {"fg_color": "transparent", "border_width": 0},
        }
        style = variants.get(variant, variants["default"])
        super().__init__(
            master,
            fg_color=style["fg_color"],
            border_color=style["border_color"],
            border_width=style["border_width"],
            corner_radius=8,
            **kwargs
        )


class ProButton(ctk.CTkButton):
    """Professional button with consistent styling."""
    
    VARIANTS = {
        "primary": {"fg_color": "#58a6ff", "hover_color": "#79b8ff", "text_color": "#ffffff", "border_width": 0},
        "secondary": {"fg_color": "#21262d", "hover_color": "#30363d", "text_color": "#e6edf3", "border_width": 1, "border_color": "#30363d"},
        "ghost": {"fg_color": "transparent", "hover_color": "#21262d", "text_color": "#e6edf3", "border_width": 0},
        "danger": {"fg_color": "#f85149", "hover_color": "#ff7b72", "text_color": "#ffffff", "border_width": 0},
        "success": {"fg_color": "#3fb950", "hover_color": "#4ac45a", "text_color": "#ffffff", "border_width": 0},
        "warning": {"fg_color": "#d29922", "hover_color": "#e3b341", "text_color": "#000000", "border_width": 0},
        "outline": {"fg_color": "transparent", "hover_color": "#21262d", "text_color": "#58a6ff", "border_width": 1, "border_color": "#58a6ff"},
    }
    
    def __init__(self, master, variant: str = "primary", size: str = "md", **kwargs):
        style = self.VARIANTS.get(variant, self.VARIANTS["primary"])
        
        sizes = {
            "sm": {"height": 28, "font_size": 11, "corner_radius": 4, "padding": 8},
            "md": {"height": 36, "font_size": 13, "corner_radius": 6, "padding": 12},
            "lg": {"height": 44, "font_size": 14, "corner_radius": 8, "padding": 16},
            "icon": {"height": 36, "width": 36, "corner_radius": 6, "padding": 0},
        }
        size_style = sizes.get(size, sizes["md"])
        
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", style["fg_color"]),
            hover_color=kwargs.pop("hover_color", style["hover_color"]),
            text_color=kwargs.pop("text_color", style.get("text_color", "#ffffff")),
            border_width=kwargs.pop("border_width", style.get("border_width", 0)),
            border_color=kwargs.pop("border_color", style.get("border_color")),
            corner_radius=size_style["corner_radius"],
            font=ctk.CTkFont(family="Segoe UI", size=size_style["font_size"], weight="normal"),
            height=kwargs.pop("height", size_style["height"]),
            **kwargs
        )
        
        # Store size for potential use
        self._size = size
        self._variant = variant


class ProEntry(ctk.CTkEntry):
    """Professional entry field."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["code_bg"],
            border_color=COLORS["border_default"],
            text_color=COLORS["fg_primary"],
            placeholder_text_color=COLORS["fg_muted"],
            corner_radius=6,
            height=36,
            font=ctk.CTkFont(family="JetBrains Mono", size=12),
            **kwargs
        )


class ProComboBox(ctk.CTkComboBox):
    """Professional combobox."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border_default"],
            button_color=COLORS["accent_primary"],
            button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["bg_tertiary"],
            dropdown_hover_color=COLORS["bg_hover"],
            dropdown_text_color=COLORS["fg_primary"],
            text_color=COLORS["fg_primary"],
            corner_radius=6,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            dropdown_font=ctk.CTkFont(family="Segoe UI", size=12),
            height=36,
            **kwargs
        )


class ProSlider(ctk.CTkSlider):
    """Professional slider."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            progress_color=COLORS["accent_primary"],
            button_color=COLORS["accent_primary"],
            button_hover_color=COLORS["accent_hover"],
            corner_radius=8,
            **kwargs
        )


class ProSwitch(ctk.CTkSwitch):
    """Professional switch."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            progress_color=COLORS["accent_primary"],
            button_color=COLORS["accent_primary"],
            button_hover_color=COLORS["accent_hover"],
            fg_color=COLORS["border_default"],
            **kwargs
        )


class ProScrollableFrame(ctk.CTkScrollableFrame):
    """Professional scrollable frame."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border_default"],
            scrollbar_button_hover_color=COLORS["fg_muted"],
            corner_radius=0,
            **kwargs
        )


class ProTabView(ctk.CTkTabview):
    """Professional tab view."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border_default"],
            border_width=1,
            corner_radius=8,
            segmented_button_fg_color=COLORS["bg_hover"],
            segmented_button_selected_color=COLORS["accent_primary"],
            segmented_button_selected_hover_color=COLORS["accent_hover"],
            segmented_button_unselected_color=COLORS["bg_hover"],
            segmented_button_unselected_hover_color=COLORS["border_default"],
            text_color=COLORS["fg_primary"],
            **kwargs
        )


class ProLabel(ctk.CTkLabel):
    """Professional label."""
    def __init__(self, master, variant: str = "default", **kwargs):
        variants = {
            "default": {"text_color": COLORS["fg_primary"], "font_size": 13},
            "secondary": {"text_color": COLORS["fg_secondary"], "font_size": 12},
            "muted": {"text_color": COLORS["fg_muted"], "font_size": 12},
            "heading": {"text_color": COLORS["fg_primary"], "font_size": 16, "weight": "bold"},
            "title": {"text_color": COLORS["accent_primary"], "font_size": 14, "weight": "bold"},
            "caption": {"text_color": COLORS["fg_muted"], "font_size": 11},
            "code": {"text_color": COLORS["fg_primary"], "font_size": 11, "font_family": "JetBrains Mono"},
        }
        style = variants.get(variant, variants["default"])
        super().__init__(
            master,
            text_color=style["text_color"],
            font=ctk.CTkFont(
                family=style.get("font_family", "Segoe UI"),
                size=style["font_size"],
                weight=style.get("weight", "normal")
            ),
            **kwargs
        )


class ProSeparator(ctk.CTkFrame):
    """Professional separator."""
    def __init__(self, master, orientation: str = "horizontal", **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["border_default"],
            height=1 if orientation == "horizontal" else 2,
            width=2 if orientation == "vertical" else 2,
            **kwargs
        )


class ProScrollbar(ctk.CTkScrollbar):
    """Professional scrollbar."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["bg_tertiary"],
            button_color=COLORS["border_default"],
            button_hover_color=COLORS["fg_muted"],
            corner_radius=0,
            **kwargs
        )


# ════════════════════════════════════════════════════════════════════
# Composite Widgets
# ════════════════════════════════════════════════════════════════════

class ProCard(ctk.CTkFrame):
    """Card widget with hover effect."""
    def __init__(self, master, on_click: Callable = None, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border_default"],
            border_width=1,
            corner_radius=8,
            **kwargs
        )
        self._on_click = on_click
        self._default_border = COLORS["border_default"]
        self._hover_border = COLORS["accent_primary"]
        self._selected_border = COLORS["accent_primary"]
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        if on_click:
            self.bind("<Button-1>", lambda e: on_click())
            for child in self.winfo_children():
                child.bind("<Button-1>", lambda e: on_click())
                
    def _on_enter(self, event):
        if not getattr(self, '_selected', False):
            self.configure(border_color=COLORS["accent_dim"])
            
    def _on_leave(self, event):
        if not getattr(self, '_selected', False):
            self.configure(border_color=COLORS["border_default"])
            
    def set_selected(self, selected: bool):
        self._selected = selected
        self.configure(
            border_color=COLORS["accent_primary"] if selected else COLORS["border_default"],
            border_width=2 if selected else 1
        )


class ProIconButton(ctk.CTkButton):
    """Icon-only button for toolbars."""
    def __init__(self, master, text: str = "", variant: str = "ghost", size: str = "sm", **kwargs):
        sizes = {
            "xs": {"height": 24, "width": 24, "font_size": 10, "corner_radius": 4},
            "sm": {"height": 28, "width": 28, "font_size": 12, "corner_radius": 4},
            "md": {"height": 36, "width": 36, "font_size": 14, "corner_radius": 6},
            "lg": {"height": 44, "width": 44, "font_size": 16, "corner_radius": 8},
        }
        size_style = sizes.get(size, sizes["sm"])
        
        variants = {
            "ghost": {"fg_color": "transparent", "hover_color": "#21262d", "text_color": "#e6edf3", "border_width": 0},
            "primary": {"fg_color": "#58a6ff", "hover_color": "#79b8ff", "text_color": "#fff", "border_width": 0},
            "secondary": {"fg_color": "#21262d", "hover_color": "#30363d", "text_color": "#e6edf3", "border_width": 1, "border_color": "#30363d"},
        }
        style = {k: v for k, v in variants.get(variant, variants["ghost"]).items() if k != "text_color"}
        
        super().__init__(
            master,
            text=text,
            fg_color="transparent",
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["fg_primary"],
            border_width=0,
            corner_radius=4,
            height=size_style["height"],
            width=size_style["width"],
            font=ctk.CTkFont(family="Segoe UI", size=size_style["font_size"]),
            **kwargs
        )
        self.configure(width=size_style["width"], height=size_style["height"])


class ProTooltip:
    """Tooltip for widgets."""
    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None
        
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<Motion>", self._on_motion)
        
    def _on_enter(self, event):
        self.after_id = self.widget.after(self.delay, self._show_tooltip)
        
    def _on_leave(self, event):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self._hide_tooltip()
        
    def _on_motion(self, event):
        if self.tooltip_window:
            self._position_tooltip(event)
            
    def _show_tooltip(self):
        if self.tooltip_window:
            return
            
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#21262d",
            foreground="#e6edf3",
            font=("Segoe UI", 11),
            padx=8,
            pady=4,
            relief="solid",
            borderwidth=1,
            highlightbackground="#30363d"
        )
        label.pack()
        
    def _position_tooltip(self, event):
        if self.tooltip_window:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + 20
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
    def _hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def add_tooltip(widget: tk.Widget, text: str, delay: int = 500) -> ProTooltip:
    """Add tooltip to a widget."""
    return ProTooltip(widget, text, delay)


# ════════════════════════════════════════════════════════════════════
# Layout Helpers
# ════════════════════════════════════════════════════════════════════

def create_toolbar(master, **kwargs) -> ctk.CTkFrame:
    """Create a toolbar frame."""
    return ctk.CTkFrame(master, fg_color="transparent", height=44, **kwargs)


def create_status_bar(master, **kwargs) -> ctk.CTkFrame:
    """Create a status bar."""
    frame = ctk.CTkFrame(master, fg_color="#161b22", height=28, corner_radius=0, border_width=1, border_color="#30363d", **kwargs)
    frame.pack_propagate(False)
    return frame


def create_paned_window(master, orient: str = "horizontal", **kwargs) -> ctk.CTkFrame:
    """Create a paned window container."""
    return ctk.CTkFrame(master, fg_color="transparent", **kwargs)


def grid_configure(widget, rows: list = None, cols: list = None):
    """Configure grid weights for rows and columns."""
    if rows:
        for i, weight in enumerate(rows):
            widget.grid_rowconfigure(i, weight=weight)
    if cols:
        for i, weight in enumerate(cols):
            widget.grid_columnconfigure(i, weight=weight)


def pack_toolbar_buttons(frame, buttons: list, side: str = "left", padx: int = 4):
    """Pack toolbar buttons with consistent spacing."""
    for btn in buttons:
        if btn is None:
            ctk.CTkFrame(frame, width=1, fg_color="#30363d").pack(side=side, fill="y", padx=8, pady=4)
        else:
            btn.pack(side=side, padx=2, pady=4)


# ════════════════════════════════════════════════════════════════════
# Dialog Helpers
# ════════════════════════════════════════════════════════════════════

def show_info(title: str, message: str, parent=None):
    """Show info dialog."""
    return messagebox.showinfo(title, message, parent=parent)


def show_warning(title: str, message: str, parent=None):
    return messagebox.showwarning(title, message, parent=parent)


def show_error(title: str, message: str, parent=None):
    return messagebox.showerror(title, message, parent=parent)


def ask_yes_no(title: str, message: str, parent=None) -> bool:
    return messagebox.askyesno(title, message, parent=parent)


def ask_yes_no_cancel(title: str, message: str, parent=None):
    return messagebox.askyesnocancel(title, message, parent=parent)


def ask_string(title: str, prompt: str, initial: str = "", parent=None) -> Optional[str]:
    return simpledialog.askstring(title, prompt, initialvalue=initial, parent=parent)


def ask_integer(title: str, prompt: str, initial: int = 0, min_val: int = None, max_val: int = None, parent=None) -> Optional[int]:
    return simpledialog.askinteger(title, prompt, initialvalue=initial, minvalue=min_val, maxvalue=max_val, parent=parent)


def ask_float(title: str, prompt: str, initial: float = 0.0, min_val: float = None, max_val: float = None, parent=None) -> Optional[float]:
    return simpledialog.askfloat(title, prompt, initialvalue=initial, minvalue=min_val, maxvalue=max_val, parent=parent)