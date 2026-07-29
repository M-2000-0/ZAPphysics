"""
ZapPhysics Professional — Settings & Theme Management
Centralized configuration with persistence.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading


class ThemeMode(Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


@dataclass
class EditorSettings:
    font_family: str = "JetBrains Mono"
    font_size: int = 13
    line_numbers: bool = True
    word_wrap: bool = False
    tab_size: int = 4
    auto_indent: bool = True
    highlight_current_line: bool = True
    show_whitespace: bool = False
    minimap: bool = False


@dataclass
class ConsoleSettings:
    font_family: str = "JetBrains Mono"
    font_size: int = 11
    auto_scroll: bool = True
    max_lines: int = 10000
    ansi_colors: bool = True
    timestamps: bool = False


@dataclass
class VisualizationSettings:
    theme: str = "dark"
    dpi: int = 100
    antialiasing: bool = True
    grid: bool = True
    legend: bool = True
    toolbar: bool = True


@dataclass
class SimulationSettings:
    default_dt: float = 0.01
    default_max_time: float = 10.0
    max_history: int = 5000
    auto_run_on_load: bool = False
    show_performance: bool = True


@dataclass
class AppSettings:
    theme_mode: ThemeMode = ThemeMode.SYSTEM
    theme_name: str = "zapphysics"  # custom theme
    window_geometry: str = "1700x1050"
    window_state: str = "normal"  # normal, maximized, fullscreen
    splitter_positions: Dict[str, int] = field(default_factory=dict)
    recent_files: list = field(default_factory=list)
    max_recent_files: int = 10
    
    editor: EditorSettings = field(default_factory=EditorSettings)
    console: ConsoleSettings = field(default_factory=ConsoleSettings)
    visualization: VisualizationSettings = field(default_factory=VisualizationSettings)
    simulation: SimulationSettings = field(default_factory=SimulationSettings)
    
    # UI preferences
    show_sidebar: bool = True
    show_console: bool = True
    show_parameters: bool = True
    show_toolbar: bool = True
    show_statusbar: bool = True
    confirm_exit: bool = True
    auto_save: bool = True
    auto_save_interval: int = 30  # seconds


class SettingsManager:
    """Manages application settings with file persistence."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path.home() / ".zapphysics"
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "settings.json"
        self._lock = threading.RLock()
        self._settings: Optional[AppSettings] = None
        self._watchers: list = []
        
    def load(self) -> AppSettings:
        """Load settings from file, with fallback to defaults."""
        with self._lock:
            if self._settings is not None:
                return self._settings
                
            if self.config_file.exists():
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self._settings = self._deserialize(data)
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    print(f"Warning: Failed to load settings, using defaults: {e}")
                    self._settings = AppSettings()
            else:
                self._settings = AppSettings()
                
            return self._settings
    
    def save(self) -> bool:
        """Save current settings to file."""
        with self._lock:
            if self._settings is None:
                return False
            try:
                data = self._serialize(self._settings)
                # Atomic write
                temp_file = self.config_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                temp_file.replace(self.config_file)
                return True
            except Exception as e:
                print(f"Error saving settings: {e}")
                return False
    
    def get(self) -> AppSettings:
        """Get current settings (load if needed)."""
        if self._settings is None:
            self.load()
        return self._settings
    
    def update(self, **kwargs) -> None:
        """Update settings and save."""
        settings = self.get()
        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        self.save()
        self._notify_watchers()
    
    def update_nested(self, section: str, **kwargs) -> None:
        """Update nested settings section."""
        settings = self.get()
        if hasattr(settings, section):
            section_obj = getattr(settings, section)
            for key, value in kwargs.items():
                if hasattr(section_obj, key):
                    setattr(section_obj, key, value)
        self.save()
        self._notify_watchers()
    
    def add_recent_file(self, path: str) -> None:
        """Add file to recent files list."""
        settings = self.get()
        if path in settings.recent_files:
            settings.recent_files.remove(path)
        settings.recent_files.insert(0, path)
        settings.recent_files = settings.recent_files[:settings.max_recent_files]
        self.save()
    
    def watch(self, callback) -> None:
        """Register a callback for settings changes."""
        self._watchers.append(callback)
    
    def _notify_watchers(self) -> None:
        for callback in self._watchers:
            try:
                callback(self._settings)
            except Exception as e:
                print(f"Settings watcher error: {e}")
    
    def _serialize(self, settings: AppSettings) -> Dict[str, Any]:
        data = asdict(settings)
        # Convert enums
        data['theme_mode'] = settings.theme_mode.value
        return data
    
    def _deserialize(self, data: Dict[str, Any]) -> AppSettings:
        # Convert enums
        if 'theme_mode' in data:
            data['theme_mode'] = ThemeMode(data['theme_mode'])
        
        # Nested objects
        if 'editor' in data:
            data['editor'] = EditorSettings(**data['editor'])
        if 'console' in data:
            data['console'] = ConsoleSettings(**data['console'])
        if 'visualization' in data:
            data['visualization'] = VisualizationSettings(**data['visualization'])
        if 'simulation' in data:
            data['simulation'] = SimulationSettings(**data['simulation'])
        
        return AppSettings(**data)


# Global instance
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager(config_dir: Optional[Path] = None) -> SettingsManager:
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager(config_dir)
    return _settings_manager


def get_settings() -> AppSettings:
    return get_settings_manager().load()