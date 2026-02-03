"""
Game Macro Recorder - Core recording and playback functionality
"""
import time
import json
from pynput import mouse, keyboard as pynput_keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController


class MacroRecorder:
    """Records and plays back mouse and keyboard actions"""
    
    def __init__(self):
        self.events = []
        self.recording = False
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
    def start_recording(self):
        """Start recording mouse and keyboard events"""
        self.events = []
        self.recording = True
        self.start_time = time.time()
        
        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll
        )
        
        # Start keyboard listener
        self.keyboard_listener = pynput_keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
    def stop_recording(self):
        """Stop recording events"""
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        return self.events
    
    def _record_event(self, event_type, data):
        """Record an event with timestamp"""
        if not self.recording:
            return
        
        timestamp = time.time() - self.start_time
        self.events.append({
            'timestamp': timestamp,
            'type': event_type,
            'data': data
        })
    
    def _on_mouse_move(self, x, y):
        """Handle mouse move events"""
        self._record_event('mouse_move', {'x': x, 'y': y})
    
    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        button_name = button.name if hasattr(button, 'name') else str(button)
        self._record_event('mouse_click', {
            'x': x,
            'y': y,
            'button': button_name,
            'pressed': pressed
        })
    
    def _on_mouse_scroll(self, x, y, dx, dy):
        """Handle mouse scroll events"""
        self._record_event('mouse_scroll', {
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy
        })
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            key_char = key.char if hasattr(key, 'char') else key.name
        except AttributeError:
            key_char = str(key)
        
        self._record_event('key_press', {'key': key_char})
    
    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            key_char = key.char if hasattr(key, 'char') else key.name
        except AttributeError:
            key_char = str(key)
        
        self._record_event('key_release', {'key': key_char})
    
    def playback(self, events, speed=1.0):
        """Play back recorded events"""
        if not events:
            return
        
        mouse_ctrl = MouseController()
        keyboard_ctrl = KeyboardController()
        
        start_time = time.time()
        
        for event in events:
            # Wait for the event timestamp
            target_time = event['timestamp'] / speed
            elapsed = time.time() - start_time
            
            if target_time > elapsed:
                time.sleep(target_time - elapsed)
            
            # Execute the event
            event_type = event['type']
            data = event['data']
            
            try:
                if event_type == 'mouse_move':
                    mouse_ctrl.position = (data['x'], data['y'])
                
                elif event_type == 'mouse_click':
                    button_map = {
                        'left': Button.left,
                        'right': Button.right,
                        'middle': Button.middle
                    }
                    button = button_map.get(data['button'], Button.left)
                    
                    if data['pressed']:
                        mouse_ctrl.press(button)
                    else:
                        mouse_ctrl.release(button)
                
                elif event_type == 'mouse_scroll':
                    mouse_ctrl.scroll(data['dx'], data['dy'])
                
                elif event_type == 'key_press':
                    key = self._get_key(data['key'])
                    if key:
                        keyboard_ctrl.press(key)
                
                elif event_type == 'key_release':
                    key = self._get_key(data['key'])
                    if key:
                        keyboard_ctrl.release(key)
            except Exception as e:
                print(f"Error playing back event: {e}")
    
    def _get_key(self, key_str):
        """Convert key string to Key object"""
        # Try to get special key
        try:
            return getattr(Key, key_str)
        except AttributeError:
            pass
        
        # Return as character
        if len(key_str) == 1:
            return key_str
        
        # Handle Key. prefix
        if key_str.startswith('Key.'):
            key_name = key_str.replace('Key.', '')
            try:
                return getattr(Key, key_name)
            except AttributeError:
                pass
        
        return key_str
    
    def save_to_file(self, filename):
        """Save recorded events to a file"""
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def load_from_file(self, filename):
        """Load recorded events from a file"""
        with open(filename, 'r') as f:
            self.events = json.load(f)
        return self.events
