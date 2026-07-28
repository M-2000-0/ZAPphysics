"""Dark theme color palette and styling for Tkinter."""
from tkinter import ttk

DARK_COLORS = {
    "bg": "#1e1e1e",           # Main background
    "panel": "#252526",        # Panel/widget background
    "panel_light": "#2d2d2d",  # Lighter panel
    "fg": "#d4d4d4",           # Main text
    "fg_dim": "#858585",       # Dimmed text
    "accent": "#007acc",       # Accent blue
    "accent_hover": "#1a8cff", # Accent hover
    "accent_dim": "#005a9e",   # Accent dimmed
    "error": "#f14c4c",        # Error red
    "success": "#4ec9b0",      # Success teal
    "warning": "#ffd700",      # Warning gold
    "info": "#569cd6",         # Info blue
    "border": "#3c3c3c",       # Border color
    "selection": "#264f78",    # Selection highlight
    "line_number": "#3e3e3e",  # Line number background
    "console_bg": "#101010",   # Console background
}

# Export individual constants for convenience
BG = DARK_COLORS["bg"]
PANEL = DARK_COLORS["panel"]
PANEL_LIGHT = DARK_COLORS["panel_light"]
FG = DARK_COLORS["fg"]
FG_DIM = DARK_COLORS["fg_dim"]
ACCENT = DARK_COLORS["accent"]
ACCENT_HOVER = DARK_COLORS["accent_hover"]
ACCENT_DIM = DARK_COLORS["accent_dim"]
ERROR = DARK_COLORS["error"]
SUCCESS = DARK_COLORS["success"]
WARNING = DARK_COLORS["warning"]
INFO = DARK_COLORS["info"]
BORDER = DARK_COLORS["border"]
SELECTION = DARK_COLORS["selection"]
LINE_NUMBER = DARK_COLORS["line_number"]
CONSOLE_BG = DARK_COLORS["console_bg"]


def apply_dark_theme(root):
    """Apply dark theme to all ttk widgets."""
    style = ttk.Style(root)
    style.theme_use('clam')

    # Configure colors
    style.configure(".",
        background=DARK_COLORS["bg"],
        foreground=DARK_COLORS["fg"],
        fieldbackground=DARK_COLORS["panel"],
        selectbackground=DARK_COLORS["selection"],
        selectforeground=DARK_COLORS["fg"],
        bordercolor=DARK_COLORS["border"],
        lightcolor=DARK_COLORS["panel_light"],
        darkcolor=DARK_COLORS["bg"],
    )

    # Frames
    style.configure("TFrame", background=DARK_COLORS["bg"])
    style.configure("TLabelframe", background=DARK_COLORS["bg"], foreground=DARK_COLORS["fg"])
    style.configure("TLabelframe.Label", background=DARK_COLORS["bg"], foreground=DARK_COLORS["accent"])

    # Labels
    style.configure("TLabel", background=DARK_COLORS["bg"], foreground=DARK_COLORS["fg"])
    style.configure("Title.TLabel", font=("Segoe UI", 11, "bold"), foreground=DARK_COLORS["accent"])

    # Buttons
    style.configure("TButton",
        background=DARK_COLORS["panel"],
        foreground=DARK_COLORS["fg"],
        borderwidth=1,
        focuscolor=DARK_COLORS["accent"],
        padding=(12, 6))
    style.map("TButton",
        background=[("active", DARK_COLORS["accent_hover"]), ("pressed", DARK_COLORS["accent_dim"])],
        foreground=[("active", DARK_COLORS["bg"]), ("pressed", DARK_COLORS["bg"])])
    
    style.configure("Accent.TButton",
        background=DARK_COLORS["accent"],
        foreground=DARK_COLORS["bg"],
        font=("Segoe UI", 9, "bold"))
    style.map("Accent.TButton",
        background=[("active", DARK_COLORS["accent_hover"]), ("pressed", DARK_COLORS["accent_dim"])])

    # Entry
    style.configure("TEntry",
        fieldbackground=DARK_COLORS["panel"],
        foreground=DARK_COLORS["fg"],
        bordercolor=DARK_COLORS["border"],
        insertcolor=DARK_COLORS["fg"],
        padding=4)
    style.map("TEntry",
        bordercolor=[("focus", DARK_COLORS["accent"])])
    
    # Combobox
    style.configure("TCombobox",
        fieldbackground=DARK_COLORS["panel"],
        foreground=DARK_COLORS["fg"],
        background=DARK_COLORS["panel"],
        arrowcolor=DARK_COLORS["fg"],
        bordercolor=DARK_COLORS["border"])
    style.map("TCombobox",
        fieldbackground=[("readonly", DARK_COLORS["panel"])],
        selectbackground=[("readonly", DARK_COLORS["selection"])],
        selectforeground=[("readonly", DARK_COLORS["fg"])])
    
    # Scale/Slider
    style.configure("Horizontal.TScale",
        background=DARK_COLORS["bg"],
        troughcolor=DARK_COLORS["panel"],
        sliderrelief="flat",
        borderwidth=0)
    style.map("Horizontal.TScale",
        background=[("active", DARK_COLORS["accent"])],
        troughcolor=[("active", DARK_COLORS["panel_light"])])

    # Notebook/Tabs
    style.configure("TNotebook", background=DARK_COLORS["bg"], borderwidth=0)
    style.configure("TNotebook.Tab",
        background=DARK_COLORS["panel"],
        foreground=DARK_COLORS["fg_dim"],
        padding=(16, 8),
        borderwidth=0)
    style.map("TNotebook.Tab",
        background=[("selected", DARK_COLORS["accent"]), ("active", DARK_COLORS["panel_light"])],
        foreground=[("selected", DARK_COLORS["bg"]), ("active", DARK_COLORS["fg"])])
    
    # Progressbar
    style.configure("TProgressbar",
        background=DARK_COLORS["accent"],
        troughcolor=DARK_COLORS["panel"],
        borderwidth=0,
        thickness=6)
    
    # Separator
    style.configure("TSeparator", background=DARK_COLORS["border"])
    
    # Scrollbar
    style.configure("Vertical.TScrollbar",
        background=DARK_COLORS["panel"],
        troughcolor=DARK_COLORS["bg"],
        bordercolor=DARK_COLORS["bg"],
        arrowcolor=DARK_COLORS["fg_dim"],
        width=12)
    style.map("Vertical.TScrollbar",
        background=[("active", DARK_COLORS["panel_light"]), ("pressed", DARK_COLORS["accent"])])
    
    style.configure("Horizontal.TScrollbar",
        background=DARK_COLORS["panel"],
        troughcolor=DARK_COLORS["bg"],
        bordercolor=DARK_COLORS["bg"],
        arrowcolor=DARK_COLORS["fg_dim"],
        height=12)
    
    # Treeview
    style.configure("Treeview",
        background=DARK_COLORS["panel"],
        foreground=DARK_COLORS["fg"],
        fieldbackground=DARK_COLORS["panel"],
        borderwidth=0,
        rowheight=24)
    style.map("Treeview",
        background=[("selected", DARK_COLORS["selection"])],
        foreground=[("selected", DARK_COLORS["fg"])])
    style.configure("Treeview.Heading",
        background=DARK_COLORS["panel_light"],
        foreground=DARK_COLORS["accent"],
        font=("Segoe UI", 9, "bold"),
        borderwidth=1)

    # Set root background
    root.configure(bg=DARK_COLORS["bg"])

    return style