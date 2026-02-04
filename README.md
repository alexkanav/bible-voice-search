# Bible Voice Search
An **offline voice-controlled Bible verse search application** built with Python. The app features a **Tkinter desktop GUI** with **Light/Dark theme support**, uses **Vosk (vosk-model-small-uk-v3)** for offline speech recognition, and retrieves Bible verses from a **local SQLite database** — no Internet connection required.

---

## Features

- **Voice-based verse search** — Speak a Bible reference instead of typing
- **Desktop GUI** — Simple and lightweight interface built with Tkinter
- **Light/Dark theme** — Choose the display mode for verse text
- **Fully offline** — No Internet, cloud APIs, or external services
- 🇺🇦 **Ukrainian speech recognition** — Powered by vosk-model-small-uk-v3
- **Local Bible storage** — Fast verse lookup using SQLite
- **Privacy-friendly** — All processing happens locally

---

## How It Works

1. The application captures audio from the microphone
2. Converts speech to text using **Vosk (offline ASR)**
3. Parses the spoken Bible reference
4. Queries the verse from the **local SQLite database**
5. Displays the verse in the Tkinter GUI with the selected **Light or Dark theme**

---

## Tech Stack

- **Python**
- **Tkinter** — desktop GUI with theme support
- **Vosk** — offline speech recognition
- **vosk-model-small-uk-v3** — Ukrainian language model
- **SQLite** — local database for Bible verses
- **Standard Python libraries**

---

## Installation

```bash
git clone https://github.com/alexkanav/bible-voice-search
cd bible-voice-search
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Download Speech Recognition Model

Download and extract the Vosk Ukrainian model:
    
    vosk-model-small-uk-v3

Place it in the project directory (or update the model path in the code).

---
## Usage

```bash
python main.py
```
Speak a Bible reference, for example:
     
    Книга 5, вірш 2:4

The verse will be retrieved from the local SQLite database and displayed in the GUI. You can switch between **Light** or **Dark theme** for comfortable reading.

---

## Offline-First Design

This project is fully **offline**:

- No Internet connection required
- No external APIs or cloud services
- Ideal for privacy-focused users and low-connectivity environments

---

## Possible Improvements

- Text-to-speech to read verses aloud
- Multiple Bible translations
- Support for additional languages
- Enhanced GUI styling

---
## License
MIT License — Free to use, modify, and distribute.