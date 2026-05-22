from dataclasses import dataclass

# --- Theme Configuration ---

THEMES = {
    "dark": {
        "bg": "#2E2E2E",
        "fg": "#FFFFFF",
    },
    "light": {
        "bg": "#F9F9F9",
        "fg": "#000000",
    },
}


# --- Application Configuration ---

@dataclass(frozen=True)
class AppConfig:
    # Resources
    db_path: str = "CUV23.SQLite3"
    vosk_model_path: str = "vosk-model-small-uk-v3"

    # Runtime
    device_index: int = 1  # microphone index
    queue_timeout: float = 0.1
    log_file_path: str = "error.log"

    # Window
    title: str = "Біблія (переклад Турконяка 2020)"
    geometry: str = "800x400"

    # Labels
    label_width: int = 760
    label_height: int = 300
    label_margin: int = 10

    # Display
    max_verses: int = 5

    # Fonts
    main_font_family: str = "Courier"
    max_font_size: int = 100
    min_font_size: int = 5
    footer_font: tuple[str, int] = ("Arial", 8)
    error_font: tuple[str, int] = ("Arial", 16)
    error_fg: str = "#FF0000"

    # Theme
    theme_name: str = "dark"  # available: "dark", "light"

    @property
    def theme(self) -> dict[str, str]:
        return THEMES[self.theme_name]
