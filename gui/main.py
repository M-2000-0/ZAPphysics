"""Main application window for ZapPhysics IDE."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
import webbrowser
from pathlib import Path

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
ZAP_SRC = PROJECT_ROOT / "zap" / "src"
EXAMPLES_DIR = PROJECT_ROOT / "examples"

sys.path.insert(0, str(ZAP_SRC))

from gui.theme import *
from gui.script_editor import ScriptEditor
from gui.console import OutputConsole, ZapRunner


class ZapPhysicsIDE(ttk.Frame):
    """Main IDE window."""
    
    def __init__(self, root):
        self.root = root
        super().__init__(root)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.editor = None
        self.console = None
        self.runner = None
        
        self._build_ui()
        self._create_menu()
        self._bind_shortcuts()
        self._load_last_session()

    def _build_ui(self):
        """Build the main UI layout."""
        # Configure style
        style = ttk.Style()
        style.configure("Console.TFrame", background=PANEL)
        style.configure("Console.TLabel", background=PANEL, foreground=FG)
        
        # Main paned window (editor | console)
        self.main_paned = tk.PanedWindow(self, orient=tk.VERTICAL, 
                                          bg=BORDER, sashwidth=4, 
                                          showhandle=False)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Top: Editor area
        editor_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(editor_frame, height=400)

        # Editor toolbar
        toolbar = ttk.Frame(editor_frame)
        toolbar.pack(fill=tk.X, padx=4, pady=4)
        
        ttk.Button(toolbar, text="▶ Run", command=self.run_current, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="■ Stop", command=self.stop_run, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Button(toolbar, text="New", command=self.new_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Open", command=self.open_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Save", command=self.save_file, width=8).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="  |  ").pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="📁 Examples", command=self.open_examples, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🌐 Web", command=self.open_web_viz, width=10).pack(side=tk.LEFT, padx=2)

        # Script editor
        self.editor = ScriptEditor(editor_frame, self)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Bottom: Console
        console_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(console_frame, height=200)

        self.console = OutputConsole(console_frame)
        self.console.pack(fill=tk.BOTH, expand=True)

        # Initialize runner
        self.runner = ZapRunner(self.console)

        # Welcome message
        self.console.write_system("ZapPhysics v4.0 IDE Ready\n")
        self.console.write_system(f"Examples: {EXAMPLES_DIR}\n")
        self.console.write_system("Press F5 or click ▶ Run to execute\n\n")

    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root, bg=PANEL, fg=FG, 
                          activebackground=ACCENT, activeforeground=BG,
                          borderwidth=0)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=FG,
                           activebackground=ACCENT, activeforeground=BG)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Examples...", command=self.open_examples, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")

        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=FG,
                          activebackground=ACCENT, activeforeground=BG)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Current", command=self.run_current, accelerator="F5")
        run_menu.add_command(label="Stop", command=self.stop_run, accelerator="Shift+F5")
        run_menu.add_separator()
        run_menu.add_command(label="Run All Demos", command=self.run_all_demos)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=FG,
                           activebackground=ACCENT, activeforeground=BG)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Console", command=self.toggle_console)
        view_menu.add_command(label="Open Web Visualization", command=self.open_web_viz)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=FG,
                           activebackground=ACCENT, activeforeground=BG)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Zap Language Reference", command=self.open_docs)
        help_menu.add_command(label="GitHub Repository", command=lambda: webbrowser.open("https://github.com/M-2000-0/ZAPphysics"))
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_file_as())
        self.root.bind("<Control-e>", lambda e: self.open_examples())
        self.root.bind("<F5>", lambda e: self.run_current())
        self.root.bind("<Shift-F5>", lambda e: self.stop_run())

    def _load_last_session(self):
        """Load last opened file if any."""
        pass

    # File operations
    def new_file(self):
        self.editor.new_file()

    def open_file(self):
        path = filedialog.askopenfilename(
            defaultextension=".zap",
            filetypes=[("Zap files", "*.zap"), ("All files", "*.*")],
            initialdir=str(EXAMPLES_DIR)
        )
        if path:
            self.editor.load_file(path)

    def save_file(self):
        self.editor.save_file()

    def save_file_as(self):
        self.editor.save_file_as()

    def open_examples(self):
        """Open examples directory picker."""
        examples = sorted(EXAMPLES_DIR.glob("*.zap"))
        if not examples:
            messagebox.showinfo("No Examples", "No example files found.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Open Example")
        dialog.geometry("500x400")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Example:").pack(pady=8)
        
        listbox = tk.Listbox(dialog, bg=PANEL, fg=FG, font=("Consolas", 10),
                            selectbackground=ACCENT, borderwidth=0)
        listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        
        for ex in examples:
            listbox.insert(tk.END, ex.name)
        
        def on_select(event=None):
            sel = listbox.curselection()
            if sel:
                self.editor.load_file(str(examples[sel[0]]))
                dialog.destroy()
        
        listbox.bind("<Double-Button-1>", on_select)
        ttk.Button(dialog, text="Open", command=on_select).pack(pady=8)

    # Run operations
    def run_current(self):
        code = self.editor.get_code()
        if code.strip():
            self.console.clear()
            self.runner.run_code(code)

    def stop_run(self):
        self.runner.stop()
        self.console.write_system("\n>>> Stopped\n")

    def run_all_demos(self):
        """Run main.zap with all demos."""
        main_file = PROJECT_ROOT / "main.zap"
        if main_file.exists():
            self.console.clear()
            self.console.write_system(">>> Running all 22 demos...\n\n")
            self.runner.run_file(str(main_file))
        else:
            messagebox.showerror("Error", "main.zap not found in project root")

    def toggle_console(self):
        """Show/hide console."""
        pass

    def open_web_viz(self):
        """Open web visualization."""
        viz_dir = PROJECT_ROOT / "viz"
        if viz_dir.exists():
            # Start simple HTTP server
            import subprocess
            proc = subprocess.Popen([sys.executable, "-m", "http.server", "8080"], 
                                   cwd=str(viz_dir))
            webbrowser.open("http://localhost:8080")
            self.console.write_system(">>> Web server started at http://localhost:8080\n")
        else:
            messagebox.showinfo("Not Found", "Visualization directory not found.")

    def open_docs(self):
        """Open documentation."""
        webbrowser.open("https://github.com/M-2000-0/ZAPphysics/blob/main/README.md")

    def show_about(self):
        messagebox.showinfo("About ZapPhysics v4.0",
            "ZapPhysics v4.0 — Physics & Chemistry + Engineering Simulation\n\n"
            "22 Demos: N-body, Collision, Chemistry, EM, SPH, Rigid Body,\n"
            "Structural, Game Physics, Broadphase, Rocket, Aero, Orbital, Flight\n\n"
            "Language: Zap (custom Python-interpreted DSL)\n"
            "GitHub: https://github.com/M-2000-0/ZAPphysics")


def main():
    root = tk.Tk()
    root.title("ZapPhysics v4.0 — Physics + Chemistry + Engineering IDE")
    root.geometry("1200x800")
    root.minsize(900, 600)
    
    # Set icon if available
    try:
        root.iconbitmap(str(PROJECT_ROOT / "assets" / "icon.ico"))
    except:
        pass
    
    # Configure root background
    root.configure(bg=BG)
    
    app = ZapPhysicsIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()