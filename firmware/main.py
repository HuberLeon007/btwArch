"""
Author: Leon Huber (leonerwinhube@gmail.com)
Date: 2025-06-25

KMK Firmware configuration for a 3-button macro keypad with RGB LEDs.
Configures D0, D1, D2 pins for Alt+F4, Spotify launcher, and F5 functions.
RGB LEDs on D3 with rotating rainbow effect.

Installation:
git clone https://github.com/KMKfw/kmk_firmware.git
"""

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.extensions.RGB import RGB

def setup_keyboard():
    """
    Initialize and configure the KMK keyboard instance with RGB support.
    
    Returns:
        KMKKeyboard: Configured keyboard instance with macros, RGB, and keymap
    """
    keyboard = KMKKeyboard()
    
    # Add macros module
    macros = Macros()
    keyboard.modules.append(macros)
    
    # Add RGB extension
    rgb_ext = RGB(
        pixel_pin=board.D3,
        num_pixels=4,  # Adjust based on your LED count
        animation_mode=RGB.RAINBOW,
        val_limit=100,
        hue_default=0,
        sat_default=255,
        val_default=50,
        speed_default=10,
    )
    keyboard.extensions.append(rgb_ext)
    
    return keyboard

def configure_pins():
    """
    Define the GPIO pins used for the keypad switches.
    
    Returns:
        list: List of board pins [D0, D1, D2]
    """
    return [board.D0, board.D1, board.D2]

def create_keymap():
    """
    Created the keymap with macro definitions for each button.
    
    Button assignments:
    - D0 ~ Rage Quit:       Alt + F4 (close application)
    - D1 ~ Relax:           Open Spotify executable
    - D2 ~ Comp & Prayge:   F5 (refresh)
    
    RGB LEDs: Continuous rainbow rotation on D3
    
    Returns:
        list: Keymap configuration for the three buttons
    """
    return [
        [
            KC.Macro(Press(KC.LALT), Tap(KC.F4), Release(KC.LALT)),
            KC.MACRO("C:\\Users\\Leone\\AppData\\Roaming\\Spotify\\Spotify.exe"),
            KC.F5
        ]
    ]

keyboard = setup_keyboard()

PINS = configure_pins()

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

keyboard.keymap = create_keymap()

if __name__ == '__main__':
    """keyboard start point."""
    keyboard.go()