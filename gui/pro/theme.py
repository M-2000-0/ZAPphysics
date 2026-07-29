"""
ZapPhysics Professional — Theme System
Comprehensive theming with multiple built-in themes and custom theme support.
"""

import customtkinter as ctk
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json


class ThemeName(Enum):
    ZAP_DARK = "zapphysics_dark"
    ZAP_LIGHT = "zapphysics_light"
    GITHUB_DARK = "github_dark"
    GITHUB_LIGHT = "github_light"
    DRACULA = "dracula"
    NORD = "nord"
    SOLARIZED_DARK = "solarized_dark"
    SOLARIZED_LIGHT = "solarized_light"
    MONOKAI = "monokai"
    ONE_DARK = "one_dark"


@dataclass
class ThemeColors:
    # Base
    bg_primary: str = "#0d1117"
    bg_secondary: str = "#161b22"
    bg_tertiary: str = "#1f2428"
    bg_hover: str = "#1f2428"
    bg_active: str = "#263037"
    
    # Text
    fg_primary: str = "#e6edf3"
    fg_secondary: str = "#8b949e"
    fg_muted: str = "#6e7681"
    fg_disabled: str = "#484f58"
    
    # Accent
    accent_primary: str = "#58a6ff"
    accent_hover: str = "#79b8ff"
    accent_dim: str = "#1f6feb"
    accent_fg: str = "#ffffff"
    
    # Status
    success: str = "#3fb950"
    success_hover: str = "#4ac45a"
    warning: str = "#d29922"
    warning_hover: str = "#e3b341"
    error: str = "#f85149"
    error_hover: str = "#ff7b72"
    info: str = "#58a6ff"
    
    # Borders
    border_default: str = "#30363d"
    border_muted: str = "#21262d"
    border_focus: str = "#58a6ff"
    
    # Selection
    selection_bg: str = "#264f78"
    selection_fg: str = "#ffffff"
    selection_inactive: str = "#1f3a5f"
    
    # Code/Editor
    code_bg: str = "#0d1117"
    line_num_bg: str = "#161b22"
    line_num_fg: str = "#484f58"
    current_line_bg: str = "#1e2a38"
    selection_bg_editor: str = "#264f78"
    bracket_match_bg: str = "#1f3a5f"
    
    # Console
    console_bg: str = "#0d1117"
    console_stdout: str = "#e6edf3"
    console_stderr: str = "#f85149"
    console_system: str = "#58a6ff"
    console_success: str = "#3fb950"
    
    # Syntax highlighting
    syntax_comment: str = "#6a9955"
    syntax_keyword: str = "#c586c0"
    syntax_type: str = "#4ec9b0"
    syntax_function: str = "#dcdcaa"
    syntax_string: str = "#ce9178"
    syntax_number: str = "#b5cea8"
    syntax_operator: str = "#d4d4d4"
    syntax_bracket: str = "#d4d4d4"
    syntax_variable: str = "#9cdcfe"
    syntax_constant: str = "#4fc1ff"
    
    # Diff
    diff_add: str = "#1f3a5f"
    diff_remove: str = "#3a1d1d"
    diff_change: str = "#1f3a5f"


# Built-in themes
THEMES: Dict[str, ThemeColors] = {
    ThemeName.ZAP_DARK.value: ThemeColors(),
    
    ThemeName.ZAP_LIGHT.value: ThemeColors(
        bg_primary="#ffffff",
        bg_secondary="#f6f8fa",
        bg_tertiary="#f3f4f6",
        bg_hover="#f3f4f6",
        bg_active="#e1e4e8",
        fg_primary="#24292f",
        fg_secondary="#57606a",
        fg_muted="#6e7781",
        fg_disabled="#959da5",
        accent_primary="#0969da",
        accent_hover="#0860ca",
        accent_dim="#0550ae",
        accent_fg="#ffffff",
        success="#1a7f37",
        success_hover="#2da44e",
        warning="#9a6700",
        warning_hover="#bf8700",
        error="#cf222e",
        error_hover="#a40e26",
        border_default="#d0d7de",
        border_muted="#d8dee4",
        border_focus="#0969da",
        selection_bg="#cce0ff",
        selection_fg="#000000",
        selection_inactive="#e1e6ed",
        code_bg="#ffffff",
        line_num_bg="#f6f8fa",
        line_num_fg="#8b949e",
        current_line_bg="#f0f3f6",
        selection_bg_editor="#b4d6ff",
        bracket_match_bg="#ffd33d",
        console_bg="#ffffff",
        console_stdout="#24292f",
        console_stderr="#cf222e",
        console_system="#0969da",
        console_success="#1a7f37",
        syntax_comment="#6a9955",
        syntax_keyword="#cf222e",
        syntax_type="#0969da",
        syntax_function="#6f42c1",
        syntax_string="#a31515",
        syntax_number="#098658",
        syntax_operator="#24292f",
        syntax_bracket="#24292f",
        syntax_variable="#24292f",
        syntax_constant="#0969da",
    ),
    
    ThemeName.GITHUB_DARK.value: ThemeColors(
        bg_primary="#0d1117",
        bg_secondary="#161b22",
        bg_tertiary="#21262d",
        bg_hover="#1f2428",
        bg_active="#30363d",
        fg_primary="#e6edf3",
        fg_secondary="#8b949e",
        fg_muted="#6e7681",
        fg_disabled="#484f58",
        accent_primary="#58a6ff",
        accent_hover="#79b8ff",
        accent_dim="#1f6feb",
        success="#3fb950",
        warning="#d29922",
        error="#f85149",
        border_default="#30363d",
        border_muted="#21262d",
        border_focus="#58a6ff",
        selection_bg="#1f3a5f",
        selection_inactive="#1f3a5f",
        code_bg="#0d1117",
        line_num_bg="#161b22",
        line_num_fg="#484f58",
        current_line_bg="#1e2a38",
        selection_bg_editor="#1f3a5f",
        bracket_match_bg="#1f3a5f",
        console_bg="#0d1117",
        syntax_comment="#8b949e",
        syntax_keyword="#ff7b72",
        syntax_type="#79c0ff",
        syntax_function="#d2a8ff",
        syntax_string="#a5d6ff",
        syntax_number="#79c0ff",
        syntax_operator="#e6edf3",
        syntax_bracket="#e6edf3",
        syntax_variable="#e6edf3",
        syntax_constant="#79c0ff",
    ),
    
    ThemeName.DRACULA.value: ThemeColors(
        bg_primary="#282a36",
        bg_secondary="#282a36",
        bg_tertiary="#44475a",
        bg_hover="#44475a",
        bg_active="#6272a4",
        fg_primary="#f8f8f2",
        fg_secondary="#6272a4",
        fg_muted="#6272a4",
        accent_primary="#bd93f9",
        accent_hover="#caa9fa",
        accent_dim="#b38aff",
        success="#50fa7b",
        warning="#f1fa8c",
        error="#ff5555",
        border_default="#44475a",
        border_muted="#44475a",
        border_focus="#bd93f9",
        selection_bg="#44475a",
        code_bg="#282a36",
        line_num_bg="#282a36",
        line_num_fg="#6272a4",
        current_line_bg="#44475a",
        selection_bg_editor="#44475a",
        console_bg="#282a36",
        syntax_comment="#6272a4",
        syntax_keyword="#ff79c6",
        syntax_type="#8be9fd",
        syntax_function="#50fa7b",
        syntax_string="#f1fa8c",
        syntax_number="#bd93f9",
        syntax_operator="#ff79c6",
        syntax_bracket="#f8f8f2",
        syntax_variable="#f8f8f2",
        syntax_constant="#bd93f9",
    ),
    
    ThemeName.NORD.value: ThemeColors(
        bg_primary="#2e3440",
        bg_secondary="#3b4252",
        bg_tertiary="#434c5e",
        bg_hover="#434c5e",
        bg_active="#4c566a",
        fg_primary="#eceff4",
        fg_secondary="#d8dee9",
        fg_muted="#4c566a",
        accent_primary="#88c0d0",
        accent_hover="#8fbcbb",
        accent_dim="#81a1c1",
        success="#a3be8c",
        warning="#ebcb8b",
        error="#bf616a",
        border_default="#3b4252",
        border_muted="#3b4252",
        border_focus="#88c0d0",
        selection_bg="#3b4252",
        code_bg="#2e3440",
        line_num_bg="#3b4252",
        line_num_fg="#4c566a",
        current_line_bg="#3b4252",
        selection_bg_editor="#434c5e",
        console_bg="#2e3440",
        syntax_comment="#616e88",
        syntax_keyword="#81a1c1",
        syntax_type="#81a1c1",
        syntax_function="#88c0d0",
        syntax_string="#a3be8c",
        syntax_number="#b48ead",
        syntax_operator="#d8dee9",
        syntax_bracket="#d8dee9",
        syntax_variable="#d8dee9",
        syntax_constant="#b48ead",
    ),
    
    ThemeName.ONE_DARK.value: ThemeColors(
        bg_primary="#282c34",
        bg_secondary="#2c323c",
        bg_tertiary="#3e4451",
        bg_hover="#3e4451",
        bg_active="#3e4451",
        fg_primary="#abb2bf",
        fg_secondary="#5c6370",
        fg_muted="#5c6370",
        accent_primary="#61afef",
        accent_hover="#7ac7ff",
        accent_dim="#528bcc",
        success="#98c379",
        warning="#e5c07b",
        error="#e06c75",
        border_default="#3e4451",
        border_muted="#3e4451",
        border_focus="#61afef",
        selection_bg="#3e4451",
        code_bg="#282c34",
        line_num_bg="#2c323c",
        line_num_fg="#5c6370",
        current_line_bg="#2c323c",
        selection_bg_editor="#3e4451",
        console_bg="#282c34",
        syntax_comment="#5c6370",
        syntax_keyword="#c678dd",
        syntax_type="#e5c07b",
        syntax_function="#61afef",
        syntax_string="#98c379",
        syntax_number="#d19a66",
        syntax_operator="#56b6c2",
        syntax_bracket="#abb2bf",
        syntax_variable="#e06c75",
        syntax_constant="#d19a66",
    ),
}


# Default theme name
DEFAULT_THEME = ThemeName.ZAP_DARK.value


def get_theme(name: str = DEFAULT_THEME) -> ThemeColors:
    """Get theme by name, fallback to default."""
    return THEMES.get(name, THEMES[DEFAULT_THEME])


def list_themes() -> list:
    """List available theme names."""
    return list(THEMES.keys())


class ThemeManager:
    """Manages application theming with live switching."""
    
    def __init__(self, settings_manager=None):
        self.settings_manager = settings_manager
        self.current_theme: Optional[str] = None
        self.current_colors: Optional[ThemeColors] = None
        self._watchers: list = []
        
    def initialize(self, theme_name: Optional[str] = None):
        """Initialize theme from settings or parameter."""
        if theme_name is None and self.settings_manager:
            theme_name = self.settings_manager.get().theme_name
        theme_name = theme_name or DEFAULT_THEME
        self.apply_theme(theme_name)
        
    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme globally."""
        colors = get_theme(theme_name)
        if colors is None:
            return False
            
        self.current_theme = theme_name
        self.current_colors = colors
        
        # Apply to CustomTkinter
        self._apply_ctk_theme(colors)
        
        # Notify watchers
        self._notify_watchers()
        
        # Persist
        if self.settings_manager:
            self.settings_manager.update(theme_name=theme_name)
            
        return True
    
    def _apply_ctk_theme(self, colors: ThemeColors):
        """Apply colors to CustomTkinter widgets."""
        # This would be called to apply theme dynamically
        # CustomTkinter doesn't support full dynamic theming easily,
        # so we'd need to recreate widgets or use a custom theme file
        pass
    
    def get_colors(self) -> ThemeColors:
        return self.current_colors or get_theme()
    
    def get_current_theme(self) -> str:
        return self.current_theme or DEFAULT_THEME
    
    def watch(self, callback):
        """Register a callback for theme changes."""
        self._watchers.append(callback)
        
    def _notify_watchers(self):
        for cb in self._watchers:
            try:
                cb(self.current_colors)
            except Exception as e:
                print(f"Theme watcher error: {e}")
    
    def get_available_themes(self) -> list:
        return list(THEMES.keys())


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager