"""
ZapPhysics Professional — State Management
Centralized application state with reactive updates.
"""

from __future__ import annotations
import threading
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import weakref
import uuid


T = TypeVar('T')


class EventType(Enum):
    """Application event types."""
    # Simulation events
    SIM_START = "sim.start"
    SIM_STOP = "sim.stop"
    SIM_PAUSE = "sim.pause"
    SIM_STEP = "sim.step"
    SIM_COMPLETE = "sim.complete"
    SIM_ERROR = "sim.error"
    
    # File events
    FILE_NEW = "file.new"
    FILE_OPEN = "file.open"
    FILE_SAVE = "file.save"
    FILE_SAVE_AS = "file.save_as"
    FILE_CLOSE = "file.close"
    FILE_MODIFIED = "file.modified"
    
    # Editor events
    EDITOR_CONTENT_CHANGED = "editor.content_changed"
    EDITOR_CURSOR_MOVED = "editor.cursor_moved"
    EDITOR_SELECTION_CHANGED = "editor.selection_changed"
    
    # Simulation parameter events
    PARAMS_CHANGED = "params.changed"
    PRESET_LOADED = "preset.loaded"
    
    # Visualization events
    VIZ_CLEARED = "viz.cleared"
    VIZ_UPDATED = "viz.updated"
    VIZ_TYPE_CHANGED = "viz.type_changed"
    
    # Demo events
    DEMO_LOADED = "demo.loaded"
    DEMO_RUN_REQUESTED = "demo.run_requested"
    
    # UI events
    UI_THEME_CHANGED = "ui.theme_changed"
    UI_LAYOUT_CHANGED = "ui.layout_changed"
    UI_CONSOLE_TOGGLED = "ui.console_toggled"
    UI_PARAMS_TOGGLED = "ui.params_toggled"
    UI_VIZ_TOGGLED = "ui.viz_toggled"
    
    # Settings
    SETTINGS_CHANGED = "settings.changed"
    
    # Application
    APP_READY = "app.ready"
    APP_SHUTDOWN = "app.shutdown"


@dataclass
class Event:
    """Application event."""
    type: EventType
    data: Any = None
    source: str = ""
    timestamp: float = 0.0
    
    def __post_init__(self):
        import time
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class EventBus:
    """Central event bus for application-wide communication."""
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[Event], None]]] = {}
        self._lock = threading.RLock()
        self._event_history: List[Event] = []
        self._max_history = 1000
        
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> str:
        """Subscribe to an event type. Returns subscription ID."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            sub_id = str(uuid.uuid4())
            self._subscribers[event_type].append((sub_id, callback))
            return sub_id
        
    def unsubscribe(self, event_type: EventType, sub_id: str) -> bool:
        """Unsubscribe from an event type."""
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type] = [
                    (sid, cb) for sid, cb in self._subscribers[event_type] if sid != sub_id
                ]
                return True
            return False
        
    def publish(self, event_type: EventType, data: Any = None, source: str = "") -> None:
        """Publish an event to all subscribers."""
        event = Event(type=event_type, data=data, source=source)
        
        with self._lock:
            # Store in history
            self._event_history.append(event)
            if len(self._event_history) > self._max_history:
                self._event_history = self._event_history[-self._max_history:]
            
            # Get callbacks
            callbacks = self._subscribers.get(event_type, []).copy()
        
        # Call outside lock to avoid deadlocks
        for _, callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                import logging
                logging.getLogger("zapphysics.events").error(
                    f"Error in event callback for {event_type}: {e}"
                )
                
    def publish_async(self, event_type: EventType, data: Any = None, source: str = "") -> None:
        """Publish event asynchronously."""
        import threading
        threading.Thread(
            target=self.publish,
            args=(event_type, data, source),
            daemon=True
        ).start()
        
    def get_history(self, event_type: Optional[EventType] = None, limit: int = 100) -> List[Event]:
        """Get event history."""
        with self._lock:
            if event_type:
                return [e for e in self._event_history if e.type == event_type][-limit:]
            return self._event_history[-limit:]
        
    def clear_history(self):
        with self._lock:
            self._event_history.clear()


class Observable(Generic[T]):
    """Observable value with change notifications."""
    
    def __init__(self, value: T, on_change: Optional[Callable[[T, T], None]] = None):
        self._value = value
        self._on_change = on_change
        self._lock = threading.RLock()
        self._subscribers: List[Callable[[T, T], None]] = []
        
    @property
    def value(self) -> T:
        with self._lock:
            return self._value
            
    @value.setter
    def value(self, new_value: T):
        with self._lock:
            old_value = self._value
            if old_value != new_value:
                self._value = new_value
                # Notify subscribers
                for cb in self._subscribers:
                    try:
                        cb(new_value, old_value)
                    except Exception:
                        pass
                if self._on_change:
                    try:
                        self._on_change(new_value, old_value)
                    except Exception:
                        pass
                    
    def subscribe(self, callback: Callable[[T, T], None]) -> str:
        """Subscribe to value changes. Returns subscription ID."""
        sub_id = str(uuid.uuid4())
        with self._lock:
            self._subscribers.append(callback)
        return sub_id
        
    def unsubscribe(self, callback: Callable[[T, T], None]) -> bool:
        with self._lock:
            if callback in self._subscribers:
                self._subscribers.remove(callback)
                return True
            return False
            
    def bind(self, other: 'Observable[T]') -> str:
        """Bind to another observable (one-way)."""
        return other.subscribe(lambda new, old: setattr(self, 'value', new))


class StateManager:
    """Centralized application state management."""
    
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus
        self._lock = threading.RLock()
        self._state: Dict[str, Any] = {}
        self._observables: Dict[str, Observable] = {}
        self._subscriptions: Dict[str, str] = {}
        
        # Initialize default state
        self._init_defaults()
        
    def _init_defaults(self):
        """Initialize default state values."""
        defaults = {
            # Application
            'app.ready': False,
            'app.version': '4.2.0',
            'app.title': 'ZapPhysics Professional',
            
            # Editor
            'editor.content': '',
            'editor.file_path': None,
            'editor.modified': False,
            'editor.cursor_position': (1, 1),
            'editor.selection': None,
            'editor.font_size': 12,
            'editor.font_family': 'JetBrains Mono',
            'editor.show_line_numbers': True,
            'editor.word_wrap': False,
            'editor.tab_size': 4,
            'editor.auto_indent': True,
            
            # Simulation
            'sim.running': False,
            'sim.paused': False,
            'sim.speed': 1.0,
            'sim.current_time': 0.0,
            'sim.frame': 0,
            'sim.max_frames': 1000,
            'sim.params': {},
            
            # Visualization
            'viz.type': 'particles',
            'viz.data': None,
            'viz.params': {},
            'viz.auto_scale': True,
            'viz.show_trails': True,
            'viz.show_grid': True,
            'viz.show_axes': True,
            
            # Console
            'console.visible': True,
            'console.auto_scroll': True,
            'console.max_lines': 10000,
            
            # UI
            'ui.theme': 'zap_dark',
            'ui.sidebar_width': 300,
            'ui.console_height': 200,
            'ui.params_width': 320,
            'ui.viz_height': 400,
            'ui.show_params': True,
            'ui.show_console': True,
            'ui.show_viz': True,
            'ui.show_minimap': False,
            
            # Demo
            'demo.current': None,
            'demo.loaded': False,
            
            # Settings
            'settings.auto_save': True,
            'settings.auto_save_interval': 30,
            'settings.recent_files': [],
            'settings.max_recent_files': 10,
            'settings.check_updates': True,
            'settings.auto_check_updates': True,
        }
        
        for key, value in defaults.items():
            self._state[key] = value
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value."""
        with self._lock:
            return self._state.get(key, default)
            
    def set(self, key: str, value: Any, notify: bool = True) -> bool:
        """Set state value."""
        with self._lock:
            old_value = self._state.get(key)
            if old_value == value:
                return False
            self._state[key] = value
            
        if notify:
            self._event_bus.publish(EventType.SETTINGS_CHANGED if key.startswith('settings.') 
                                   else EventType.UI_LAYOUT_CHANGED if key.startswith('ui.')
                                   else EventType.SETTINGS_CHANGED,
                                   {'key': key, 'value': value, 'old_value': value})
        return True
        
    def update(self, updates: Dict[str, Any], notify: bool = True) -> int:
        """Update multiple values at once."""
        count = 0
        for key, value in updates.items():
            if self.set(key, value, notify=False):
                count += 1
        if notify and count > 0:
            self._event_bus.publish(EventType.SETTINGS_CHANGED, {'updates': updates})
        return count
        
    def get_observable(self, key: str) -> Observable:
        """Get or create observable for a state key."""
        with self._lock:
            if key not in self._observables:
                self._observables[key] = Observable(self._state.get(key))
                # Subscribe to state changes
                def on_change(new_val, old_val):
                    self._state[key] = new_val
                self._subscriptions[key] = self._observables[key].subscribe(on_change)
            return self._observables[key]
            
    def watch(self, key: str, callback: Callable[[Any, Any], None]) -> str:
        """Watch a state key for changes."""
        obs = self.get_observable(key)
        return obs.subscribe(callback)
        
    def unwatch(self, key: str, callback: Callable[[Any, Any], None]) -> bool:
        """Stop watching a key."""
        with self._lock:
            if key in self._observables:
                return self._observables[key].unsubscribe(callback)
            return False
            
    def get_all(self) -> Dict[str, Any]:
        """Get all state (copy)."""
        with self._lock:
            return self._state.copy()
            
    def reset(self, keys: Optional[List[str]] = None):
        """Reset state to defaults."""
        with self._lock:
            if keys is None:
                self._init_defaults()
            else:
                defaults = {
                    'editor.content': '',
                    'editor.file_path': None,
                    'editor.modified': False,
                    'sim.running': False,
                    'sim.paused': False,
                    'sim.current_time': 0.0,
                    'sim.frame': 0,
                    'viz.data': None,
                    'demo.current': None,
                    'demo.loaded': False,
                }
                for key in keys:
                    if key in defaults:
                        self._state[key] = defaults[key]


# Global instances
_event_bus: Optional[EventBus] = None
_state_manager: Optional[StateManager] = None


def get_event_bus() -> EventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


def get_state_manager() -> StateManager:
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager(get_event_bus())
    return _state_manager


def initialize_state(event_bus: Optional[EventBus] = None) -> tuple[EventBus, StateManager]:
    """Initialize global state management."""
    global _event_bus, _state_manager
    if event_bus is None:
        _event_bus = EventBus()
    else:
        _event_bus = event_bus
    _state_manager = StateManager(_event_bus)
    return _event_bus, _state_manager


# Convenience functions
def get_state(key: str, default: Any = None) -> Any:
    return get_state_manager().get(key, default)


def set_state(key: str, value: Any, notify: bool = True) -> bool:
    return get_state_manager().set(key, value, notify)


def watch_state(key: str, callback: Callable[[Any, Any], None]) -> str:
    return get_state_manager().watch(key, callback)


def publish_event(event_type: EventType, data: Any = None, source: str = "") -> None:
    get_event_bus().publish(event_type, data, source)


def subscribe_event(event_type: EventType, callback: Callable[[Event], None]) -> str:
    return get_event_bus().subscribe(event_type, callback)