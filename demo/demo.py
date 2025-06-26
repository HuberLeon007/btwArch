"""
Author: Leon Huber (leonerwinhube@gmail.com)
Date: 2025-06-26

CustomTkinter-based visual simulation of the hardware keypad functionality.
"""

import customtkinter as ctk
import math
import colorsys
import threading
import time


class MacroKeypadSimulator:
    """
    CustomTkinter-based simulation of a 3-button macro keypad with RGB LED.
    
    Simulates the behavior of a physical keypad with:
    - 3 macro buttons (Alt+F4, Spotify, F5)
    - Rainbow rotating RGB LED
    - Visual feedback for button presses
    """
    
    def __init__(self):
        """Initialize the keypad simulator window and components."""
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.start_rainbow_animation()
    
    def setup_window(self):
        """Configure the main application window."""
        self.root = ctk.CTk()
        self.root.title("KMK Macro Keypad Simulator")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def setup_variables(self):
        """Initialize animation and state variables."""
        self.hue = 0.0
        self.animation_running = True
        self.action_text = ""
    
    def hsv_to_hex(self, h, s, v):
        """
        Convert HSV color values to hexadecimal color string.
        
        Args:
            h (float): Hue value (0-1)
            s (float): Saturation value (0-1)
            v (float): Value/brightness (0-1)
            
        Returns:
            str: Hexadecimal color string
        """
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
    
    def create_widgets(self):
        """Create and arrange all UI components."""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="btwArch Hackpad Demo", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # RGB LED (simulated as a colored circle)
        self.led_frame = ctk.CTkFrame(main_frame, width=80, height=80, corner_radius=40)
        self.led_frame.pack(pady=(0, 40))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        # Create the three macro buttons with 3D appearance and vibrant colors
        self.button1 = ctk.CTkButton(
            buttons_frame,
            text="Rage\nQuit",
            width=120,
            height=120,
            corner_radius=12,
            border_width=3,
            border_color="#cc6666",
            command=lambda: self.button_press("Alt+F4 (Close Application)"),
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#994444",
            hover_color="#773333",
            text_color="#ffffff"
        )
        self.button1.grid(row=0, column=0, padx=15)
        
        self.button2 = ctk.CTkButton(
            buttons_frame,
            text="Relax",
            width=120,
            height=120,
            corner_radius=12,
            border_width=3,
            border_color="#66cc66",
            command=lambda: self.button_press("Opening Spotify..."),
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#449944",
            hover_color="#337733",
            text_color="#ffffff"
        )
        self.button2.grid(row=0, column=1, padx=15)
        
        self.button3 = ctk.CTkButton(
            buttons_frame,
            text="Comp\n&\nPrayge",
            width=120,
            height=120,
            corner_radius=12,
            border_width=3,
            border_color="#6666cc",
            command=lambda: self.button_press("F5 (Refresh)"),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#444499",
            hover_color="#333377",
            text_color="#ffffff"
        )
        self.button3.grid(row=0, column=2, padx=15)
        
        # Add shadow effect by creating shadow frames behind buttons
        shadow1 = ctk.CTkFrame(buttons_frame, width=124, height=124, corner_radius=12, fg_color="#1a1a1a")
        shadow1.grid(row=0, column=0, padx=15, pady=4, sticky="se")
        shadow1.lower()
        
        shadow2 = ctk.CTkFrame(buttons_frame, width=124, height=124, corner_radius=12, fg_color="#1a1a1a")
        shadow2.grid(row=0, column=1, padx=15, pady=4, sticky="se")
        shadow2.lower()
        
        shadow3 = ctk.CTkFrame(buttons_frame, width=124, height=124, corner_radius=12, fg_color="#1a1a1a")
        shadow3.grid(row=0, column=2, padx=15, pady=4, sticky="se")
        shadow3.lower()
        
        # Status display
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready...",
            font=ctk.CTkFont(size=18)
        )
        self.status_label.pack(pady=(40, 20))

    def show_action_popup(self, action):
        """
        Show action feedback in a separate popup window.
        
        Args:
            action (str): Description of the action performed
        """
        popup = ctk.CTkToplevel(self.root)
        popup.title("Action Performed")
        popup.geometry("400x200")
        popup.resizable(False, False)
        
        # Center the popup relative to main window
        popup.transient(self.root)
        popup.grab_set()
        
        # Action label
        action_label = ctk.CTkLabel(
            popup,
            text=f"Action: {action}",
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=350
        )
        action_label.pack(expand=True, pady=30)
        
        # Close button
        close_btn = ctk.CTkButton(
            popup,
            text="OK",
            width=120,
            height=40,
            command=popup.destroy
        )
        close_btn.pack(pady=(0, 30))
        
        # Auto-close after 3 seconds
        popup.after(3000, popup.destroy)
    
    def button_press(self, action):
        """
        Handle button press events and display action feedback.
        
        Args:
            action (str): Description of the action performed
        """
        self.status_label.configure(text="Button pressed!")
        self.show_action_popup(action)
        
        # Reset status text after 1 second
        self.root.after(1000, lambda: self.status_label.configure(text="Ready..."))
    
    def update_rainbow(self):
        """Update the RGB LED color for rainbow animation."""
        if not self.animation_running:
            return
            
        # Convert HSV to hex color
        color = self.hsv_to_hex(self.hue, 1.0, 1.0)
        
        # Update LED frame color
        self.led_frame.configure(fg_color=color)
        
        # Increment hue for next frame
        self.hue += 0.01
        if self.hue >= 1.0:
            self.hue = 0.0
        
        # Schedule next update
        self.root.after(50, self.update_rainbow)
    
    def start_rainbow_animation(self):
        """Start the rainbow LED animation."""
        self.update_rainbow()
    
    def run(self):
        """Start the main application loop."""
        self.root.mainloop()
        self.animation_running = False


def main():
    """
    Main entry point for the macro keypad simulator.
    
    Creates and runs the simulator application.
    """
    simulator = MacroKeypadSimulator()
    simulator.run()


if __name__ == "__main__":
    main()
