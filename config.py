DB_PATH = 'CUV23.SQLite3'

DEVICE_INDEX = 1  # microphone

MODEL_PATH = "vosk-model-small-uk-v3"

LOG_FILE_PATH = 'error.log'

WIDTH = 600
HEIGHT = 300

QUEUE_TIMEOUT = 0.1

FONT_FAMILY = "Courier"
FONT_SMALL = ("Arial", 8)

THEME = "dark"  # or "light"

if THEME == "dark":
    BG_COLOR = "#2e2e2e"
    FONT_COLOR = "#ffffff"
else:
    BG_COLOR = "#f9f9f9"
    FONT_COLOR = "#000000"
