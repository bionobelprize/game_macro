"""
Game Macro Recorder - Graphical User Interface
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import keyboard
import threading
import json
import os
from macro_recorder import MacroRecorder


class MacroGUI:
    """Graphical interface for macro configuration and control"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Macro Recorder")
        self.window.geometry("800x600")
        
        self.recorder = MacroRecorder()
        self.macros = {}  # Dictionary to store multiple macros
        self.current_macro = None
        self.is_recording = False
        self.playback_thread = None
        
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="Game Macro Recorder", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Macro list section
        ttk.Label(main_frame, text="Macro List:", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, 
                                                  sticky=tk.W, pady=5)
        
        # Macro listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.macro_listbox = tk.Listbox(list_frame, height=8, 
                                        yscrollcommand=scrollbar.set)
        self.macro_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.macro_listbox.yview)
        
        self.macro_listbox.bind('<<ListboxSelect>>', self.on_macro_select)
        
        # Macro details section
        details_frame = ttk.LabelFrame(main_frame, text="Macro Details", padding="10")
        details_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        details_frame.columnconfigure(1, weight=1)
        
        # Macro name
        ttk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(details_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Hotkey
        ttk.Label(details_frame, text="Hotkey:").grid(row=1, column=0, sticky=tk.W, pady=5)
        hotkey_container = ttk.Frame(details_frame)
        hotkey_container.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.hotkey_entry = ttk.Entry(hotkey_container, width=30)
        self.hotkey_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Add help text with examples
        hotkey_help = ttk.Label(details_frame, text="Examples: alt+1, ctrl+shift+2, f1", 
                               font=('Arial', 8), foreground='gray')
        hotkey_help.grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Speed
        ttk.Label(details_frame, text="Playback Speed:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_frame = ttk.Frame(details_frame)
        speed_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.speed_scale = ttk.Scale(speed_frame, from_=0.1, to=5.0, 
                                     variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(side=tk.LEFT, padx=5)
        self.speed_var.trace('w', self.update_speed_label)
        
        # Event count
        ttk.Label(details_frame, text="Events:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.events_label = ttk.Label(details_frame, text="0")
        self.events_label.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.record_btn = ttk.Button(button_frame, text="Start Recording", 
                                     command=self.toggle_recording, width=15)
        self.record_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = ttk.Button(button_frame, text="Play Macro", 
                                   command=self.play_macro, width=15)
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.save_btn = ttk.Button(button_frame, text="Save Macro", 
                                   command=self.save_macro, width=15)
        self.save_btn.grid(row=0, column=2, padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="Delete Macro", 
                                     command=self.delete_macro, width=15)
        self.delete_btn.grid(row=0, column=3, padx=5)
        
        # File operations
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(file_frame, text="Import Macro", 
                  command=self.import_macro, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Export Macro", 
                  command=self.export_macro, width=15).grid(row=0, column=1, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(2, weight=1)
        
    def update_speed_label(self, *args):
        """Update speed label when scale changes"""
        speed = self.speed_var.get()
        self.speed_label.config(text=f"{speed:.1f}x")
    
    def on_macro_select(self, event):
        """Handle macro selection from list"""
        selection = self.macro_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        macro_name = self.macro_listbox.get(index)
        
        if macro_name in self.macros:
            macro = self.macros[macro_name]
            self.current_macro = macro_name
            
            # Update UI
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, macro_name)
            
            self.hotkey_entry.delete(0, tk.END)
            self.hotkey_entry.insert(0, macro.get('hotkey', ''))
            
            self.speed_var.set(macro.get('speed', 1.0))
            
            events = macro.get('events', [])
            self.events_label.config(text=str(len(events)))
    
    def toggle_recording(self):
        """Start or stop recording"""
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.record_btn.config(text="Stop Recording")
            self.status_var.set("Recording... Press 'Stop Recording' to finish")
            
            # Disable other buttons during recording
            self.play_btn.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.DISABLED)
            
            self.recorder.start_recording()
        else:
            # Stop recording
            events = self.recorder.stop_recording()
            self.is_recording = False
            self.record_btn.config(text="Start Recording")
            self.status_var.set(f"Recording stopped. Captured {len(events)} events")
            
            # Re-enable buttons
            self.play_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            
            # Store events temporarily
            name = self.name_entry.get() or f"Macro_{len(self.macros) + 1}"
            hotkey = self.hotkey_entry.get()
            speed = self.speed_var.get()
            
            self.macros[name] = {
                'events': events,
                'hotkey': hotkey,
                'speed': speed
            }
            
            self.current_macro = name
            self.refresh_macro_list()
            self.events_label.config(text=str(len(events)))
    
    def play_macro(self):
        """Play the selected macro"""
        if not self.current_macro or self.current_macro not in self.macros:
            messagebox.showwarning("Warning", "Please select a macro to play")
            return
        
        macro = self.macros[self.current_macro]
        events = macro.get('events', [])
        speed = macro.get('speed', 1.0)
        
        if not events:
            messagebox.showwarning("Warning", "Macro has no events")
            return
        
        self.status_var.set(f"Playing macro: {self.current_macro}")
        
        # Play in separate thread to avoid blocking UI
        def play_thread():
            try:
                self.recorder.playback(events, speed)
                self.status_var.set(f"Finished playing: {self.current_macro}")
            except Exception as e:
                self.status_var.set(f"Error playing macro: {e}")
        
        self.playback_thread = threading.Thread(target=play_thread)
        self.playback_thread.daemon = True
        self.playback_thread.start()
    
    def save_macro(self):
        """Save current macro"""
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Warning", "Please enter a macro name")
            return
        
        # Update or create macro
        if self.current_macro and self.current_macro in self.macros:
            events = self.macros[self.current_macro].get('events', [])
        else:
            events = []
        
        hotkey = self.hotkey_entry.get()
        speed = self.speed_var.get()
        
        # Remove old name if renamed
        if self.current_macro and self.current_macro != name and self.current_macro in self.macros:
            del self.macros[self.current_macro]
        
        self.macros[name] = {
            'events': events,
            'hotkey': hotkey,
            'speed': speed
        }
        
        self.current_macro = name
        self.refresh_macro_list()
        self.save_config()
        
        # Register hotkey if specified
        if hotkey:
            self.register_hotkey(name, hotkey)
        
        self.status_var.set(f"Saved macro: {name}")
    
    def delete_macro(self):
        """Delete selected macro"""
        if not self.current_macro or self.current_macro not in self.macros:
            messagebox.showwarning("Warning", "Please select a macro to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                               f"Delete macro '{self.current_macro}'?"):
            # Unregister hotkey
            macro = self.macros[self.current_macro]
            if macro.get('hotkey'):
                try:
                    keyboard.remove_hotkey(macro['hotkey'])
                except (KeyError, ValueError):
                    pass
            
            del self.macros[self.current_macro]
            self.current_macro = None
            self.refresh_macro_list()
            self.save_config()
            
            # Clear UI
            self.name_entry.delete(0, tk.END)
            self.hotkey_entry.delete(0, tk.END)
            self.events_label.config(text="0")
            
            self.status_var.set("Macro deleted")
    
    def import_macro(self):
        """Import macro from file"""
        filename = filedialog.askopenfilename(
            title="Import Macro",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            name = os.path.splitext(os.path.basename(filename))[0]
            name = f"Imported_{name}"
            
            # Ensure unique name
            counter = 1
            original_name = name
            while name in self.macros:
                name = f"{original_name}_{counter}"
                counter += 1
            
            self.macros[name] = {
                'events': data,
                'hotkey': '',
                'speed': 1.0
            }
            
            self.current_macro = name
            self.refresh_macro_list()
            self.save_config()
            
            self.status_var.set(f"Imported macro: {name}")
            messagebox.showinfo("Success", f"Macro imported as '{name}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import macro: {e}")
    
    def export_macro(self):
        """Export selected macro to file"""
        if not self.current_macro or self.current_macro not in self.macros:
            messagebox.showwarning("Warning", "Please select a macro to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Macro",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"{self.current_macro}.json"
        )
        
        if not filename:
            return
        
        try:
            macro = self.macros[self.current_macro]
            events = macro.get('events', [])
            
            with open(filename, 'w') as f:
                json.dump(events, f, indent=2)
            
            self.status_var.set(f"Exported macro: {self.current_macro}")
            messagebox.showinfo("Success", "Macro exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export macro: {e}")
    
    def refresh_macro_list(self):
        """Refresh the macro list display"""
        self.macro_listbox.delete(0, tk.END)
        for name in sorted(self.macros.keys()):
            self.macro_listbox.insert(tk.END, name)
        
        # Select current macro
        if self.current_macro:
            try:
                index = sorted(self.macros.keys()).index(self.current_macro)
                self.macro_listbox.selection_set(index)
            except ValueError:
                pass
    
    def validate_hotkey(self, hotkey):
        """Validate hotkey format and check if it's supported"""
        if not hotkey or not hotkey.strip():
            return True, ""  # Empty is valid (no hotkey)
        
        hotkey = hotkey.strip().lower()
        
        # Check for valid characters
        valid_modifiers = ['ctrl', 'alt', 'shift', 'win', 'cmd']
        valid_separators = ['+', ' ']
        
        # Split by + to get key parts
        parts = [p.strip() for p in hotkey.split('+')]
        
        if len(parts) == 0:
            return False, "Hotkey cannot be empty"
        
        # Validate each part
        for part in parts:
            if not part:
                return False, "Invalid hotkey format (empty part)"
        
        # Examples of valid hotkeys: 
        # - Single keys: a, 1, f1, space, enter
        # - Combinations: ctrl+a, alt+1, ctrl+shift+f1
        # The keyboard library is quite permissive, so we just check basic format
        
        return True, ""
    
    def register_hotkey(self, macro_name, hotkey):
        """Register a hotkey for a macro"""
        if not hotkey:
            return
        
        # Validate hotkey format
        is_valid, error_msg = self.validate_hotkey(hotkey)
        if not is_valid:
            error_detail = f"Invalid hotkey format: {error_msg}\n\n"
            error_detail += "Valid formats:\n"
            error_detail += "- Single keys: a, 1, f1, space\n"
            error_detail += "- Combinations: alt+1, ctrl+shift+2, ctrl+alt+f1"
            messagebox.showerror("Invalid Hotkey", error_detail)
            return
        
        try:
            # Remove existing hotkey if any
            try:
                keyboard.remove_hotkey(hotkey)
            except (KeyError, ValueError):
                pass
            
            # Register new hotkey
            def play_callback():
                if macro_name in self.macros:
                    macro = self.macros[macro_name]
                    events = macro.get('events', [])
                    speed = macro.get('speed', 1.0)
                    
                    if events:
                        threading.Thread(
                            target=lambda: self.recorder.playback(events, speed),
                            daemon=True
                        ).start()
            
            keyboard.add_hotkey(hotkey, play_callback)
            self.status_var.set(f"Registered hotkey '{hotkey}' for {macro_name}")
        except Exception as e:
            error_detail = f"Failed to register hotkey '{hotkey}': {str(e)}\n\n"
            error_detail += "Common issues:\n"
            error_detail += "- The hotkey may already be in use by another application\n"
            error_detail += "- Some key names may not be recognized\n"
            error_detail += "- Try using standard modifiers: ctrl, alt, shift\n\n"
            error_detail += "Valid examples:\n"
            error_detail += "- alt+1, ctrl+1, shift+f1\n"
            error_detail += "- ctrl+shift+a, ctrl+alt+2"
            messagebox.showerror("Hotkey Registration Error", error_detail)
    
    def register_all_hotkeys(self):
        """Register hotkeys for all macros"""
        for name, macro in self.macros.items():
            hotkey = macro.get('hotkey')
            if hotkey:
                self.register_hotkey(name, hotkey)
    
    def save_config(self):
        """Save configuration to file"""
        config = {
            'macros': self.macros
        }
        
        try:
            with open('macros_config.json', 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists('macros_config.json'):
                with open('macros_config.json', 'r') as f:
                    config = json.load(f)
                
                self.macros = config.get('macros', {})
                self.refresh_macro_list()
                self.register_all_hotkeys()
                
                self.status_var.set(f"Loaded {len(self.macros)} macros")
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def run(self):
        """Start the GUI application"""
        self.window.mainloop()


def main():
    """Main entry point"""
    app = MacroGUI()
    app.run()


if __name__ == '__main__':
    main()
