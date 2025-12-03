import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys

PIN_ROWS = [board.GP8, board.GP26, board.GP27]
PIN_COLS = [board.GP1, board.GP2, board.GP4]

PIN_ENC_A = board.GP0
PIN_ENC_B = board.GP7

 


PIN_RGB = board.GP28
NUM_PIXELS = 16

PIN_SDA = board.GP6
PIN_SCL = board.GP7

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        
        self.setup_display()
        super().__init__()

    def setup_display(self):

        displayio.release_displays()

        try:
            i2c = busio.I2C(scl=PIN_SCL, sda=PIN_SDA)
            display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
            
            self.display = adafruit_displayio_ssd1306.SSD1306(
                display_bus, width=128, height=32
            )
            
            self.splash = displayio.Group()
            self.display.show(self.splash)

            text_area = label.Label(
                terminalio.FONT, text="KMK MACRO", color=0xFFFFFF, x=5, y=16
            )
            self.splash.append(text_area)
            
        except Exception as e:
            print(f"OLED Error: {e}")

keyboard = MyKeyboard()

keyboard.col_pins = PIN_COLS
keyboard.row_pins = PIN_ROWS
keyboard.diode_orientation = DiodeOrientation.COL2ROW

rgb = RGB(
    pixel_pin=PIN_RGB,
    num_pixels=NUM_PIXELS,
    val_limit=100,
    hue_default=100,
    sat_default=255,
    val_default=100,
    animation_mode=AnimationModes.RAINBOW,
)
keyboard.extensions.append(rgb)

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = ((PIN_ENC_A, PIN_ENC_B, None, False),)


encoder_handler.map = [
    ((KC.VOLU, KC.VOLD),),
]

keyboard.extensions.append(MediaKeys())

RGB_TOG = KC.RGB_TOG 
RGB_HUI = KC.RGB_HUI 
RGB_MODE = KC.RGB_M_P


keyboard.keymap = [
    [
        KC.UNDO,     KC.REDO,     KC.MUTE,
        RGB_MODE,    RGB_HUI,     RGB_TOG,
        KC.PASTE,    KC.COPY,     KC.MPLY,
    ]

]

if __name__ == '__main__':
    keyboard.go()