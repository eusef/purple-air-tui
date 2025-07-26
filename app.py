import asyncio
import threading
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Log
from textual.reactive import reactive
from textual import work
import network
import parser

class LogPanel(Log):
    """Panel for displaying log messages and sensor data"""
    
    def on_mount(self) -> None:
        """Called when the widget is mounted"""
        self.write("PurpleAir Monitor Starting...")
        self.write("Waiting for sensor data...")

class ValuePanel(Static):
    """Panel for displaying sensor values"""
    
    values = reactive({})
    
    def watch_values(self, values: dict) -> None:
        """Called when values change"""
        if not values:
            self.update("No sensor data available")
            return
            
        content = "SENSOR VALUES:\n\n"
        for key, value in values.items():
            if value is not None:
                content += f"{key}: {value}\n"
        
        self.update(content)

class PurpleAirMonitor(App):
    CSS_PATH = "monitor.css"
    
    def __init__(self):
        super().__init__()
        self.log_panel = None
        self.value_panel = None
        self.sensor_data = {}
        self.running = True

    def compose(self) -> ComposeResult:
        self.log_panel = LogPanel(id="log")
        self.value_panel = ValuePanel(id="values")
        yield Horizontal(self.log_panel, self.value_panel)

    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.start_polling()

    @work(thread=True)
    def start_polling(self) -> None:
        """Start polling the sensor in a background thread"""
        def data_callback(data: dict):
            """Callback for sensor data"""
            if "error" in data:
                self.log_panel.write(f"ERROR: {data['error']}")
                # Don't try to parse error data
                self.value_panel.values = {"Status": "Connection Error", "Error": data['error']}
                return
                
            # Parse the data
            parsed_data = parser.parse_data(data)
            self.sensor_data = parsed_data
            
            # Update UI
            self.value_panel.values = parsed_data
            self.log_panel.write(f"Received data: {len(parsed_data)} values")
            
        def debug_callback(message: str):
            """Callback for debug messages"""
            self.log_panel.write(f"DEBUG: {message}")
            
        # Start polling in a separate thread
        def poll_thread():
            try:
                network.poll_sensor(data_callback)
            except KeyboardInterrupt:
                self.running = False
                
        thread = threading.Thread(target=poll_thread, daemon=True)
        thread.start()

    def on_key(self, event):
        """Handle key events"""
        if event.key == "ctrl+c":
            self.running = False
            self.exit()

if __name__ == "__main__":
    PurpleAirMonitor().run()