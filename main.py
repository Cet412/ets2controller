from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation
import bluetooth
import threading

class ControllerLayout(BoxLayout):
    # UI elements from KV file
    bluetooth_btn = ObjectProperty(None)
    steering_wheel = ObjectProperty(None)
    steering_slider = ObjectProperty(None)
    gas_btn = ObjectProperty(None)
    brake_btn = ObjectProperty(None)
    
    # Bluetooth properties
    bluetooth_socket = None
    is_connected = False
    target_device = None  # Should be set to your PC's Bluetooth MAC address
    port = 1  # RFCOMM port
    
    # Steering properties
    steering_value = NumericProperty(0.5)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bluetooth_thread = None
        
    def try_connect_bluetooth(self):
        """Handle Bluetooth connection in a separate thread"""
        if self.is_connected:
            self.disconnect_bluetooth()
            return
            
        self.show_popup("Connecting...", "Trying to connect to Bluetooth device")
        
        # Start connection in a new thread
        self._bluetooth_thread = threading.Thread(
            target=self._connect_bluetooth_thread,
            daemon=True
        )
        self._bluetooth_thread.start()
    
    def _connect_bluetooth_thread(self):
        """Thread function for Bluetooth connection"""
        try:
            self.bluetooth_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.bluetooth_socket.connect((self.target_device, self.port))
            self.is_connected = True
            Clock.schedule_once(lambda dt: self.show_popup("Connected", "Bluetooth connection established"))
            Clock.schedule_once(lambda dt: self.update_bluetooth_ui(True))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup("Error", f"Connection failed: {str(e)}"))
            Clock.schedule_once(lambda dt: self.update_bluetooth_ui(False))
    
    def disconnect_bluetooth(self):
        """Disconnect Bluetooth"""
        try:
            if self.bluetooth_socket:
                self.bluetooth_socket.close()
            self.is_connected = False
            self.update_bluetooth_ui(False)
            self.show_popup("Disconnected", "Bluetooth disconnected")
        except Exception as e:
            self.show_popup("Error", f"Disconnection failed: {str(e)}")
    
    def update_bluetooth_ui(self, connected):
        """Update UI based on connection status"""
        with self.bluetooth_btn.canvas.before:
            self.bluetooth_btn.canvas.before.clear()
            if connected:
                Color(0, 1, 0, 0.5)  # Green
            else:
                Color(1, 0, 0, 0.5)  # Red
            Rectangle(pos=self.bluetooth_btn.pos, size=self.bluetooth_btn.size)
    
    def send_command(self, command):
        """Send command via Bluetooth"""
        if self.is_connected and self.bluetooth_socket:
            try:
                self.bluetooth_socket.send(command.encode())
            except Exception as e:
                self.show_popup("Error", f"Failed to send command: {str(e)}")
                self.disconnect_bluetooth()
    
    def on_steering_change(self, value):
        """Handle steering wheel changes"""
        self.steering_value = value
        rotation_angle = (value - 0.5) * 360  # Convert 0-1 to -180 to 180 degrees
        Animation.cancel_all(self.steering_wheel)
        Animation(angle=rotation_angle, duration=0.1).start(self.steering_wheel)
        
        # Send steering command (example: "STEER:0.75")
        if self.is_connected:
            self.send_command(f"STEER:{value:.2f}")
    
    def on_gas_press(self):
        """Handle gas pedal press"""
        with self.gas_btn.canvas.before:
            Color(0, 1, 0, 0.5)  # Green overlay
            Rectangle(pos=self.gas_btn.pos, size=self.gas_btn.size)
        self.send_command("GAS:1.0")
    
    def reset_gas_color(self):
        """Reset gas pedal appearance"""
        self.gas_btn.canvas.before.clear()
        self.send_command("GAS:0.0")
    
    def on_brake_press(self):
        """Handle brake pedal press"""
        with self.brake_btn.canvas.before:
            Color(1, 0, 0, 0.5)  # Red overlay
            Rectangle(pos=self.brake_btn.pos, size=self.brake_btn.size)
        self.send_command("BRAKE:1.0")
    
    def reset_brake_color(self):
        """Reset brake pedal appearance"""
        self.brake_btn.canvas.before.clear()
        self.send_command("BRAKE:0.0")
    
    def show_popup(self, title, message):
        """Show status popup"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

class ETS2ControllerApp(App):
    def build(self):
        # Set the target Bluetooth device (replace with your PC's MAC address)
        layout = ControllerLayout()
        layout.target_device = "00:11:22:33:44:55"  # EXAMPLE MAC, CHANGE THIS!
        return layout

if __name__ == '__main__':
    ETS2ControllerApp().run()