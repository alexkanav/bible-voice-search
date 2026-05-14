# Bible Voice Search

An **offline voice-controlled Bible verse search application** built with Python. The application features a lightweight **Tkinter desktop GUI** with adaptive text fitting and **Light/Dark theme support**, uses **Vosk (vosk-model-small-uk-v3)** for offline speech recognition, and retrieves Bible verses from a **local SQLite database** — no Internet connection required.

---

## Features

- **Voice-based verse search** — Speak a Bible reference instead of typing
- **Desktop GUI** — Simple and lightweight interface built with Tkinter
- **Light/Dark theme support** — Choose the preferred display mode
- **Fully offline** — No cloud APIs, or external services
- 🇺🇦 **Ukrainian speech recognition** — Powered by vosk-model-small-uk-v3
- **Local Bible storage** — Fast verse lookup using SQLite
- **Privacy-friendly** — All processing happens locally
- **Adaptive font sizing** for readable verse display
- **Live GUI updates** via a thread-safe queue system
- **Clean layered architecture** (GUI / Service / Repository / Parser)
- Lightweight and offline-first

---

##  Architecture

The project is structured into clear layers:

- **GUI Layer** (`BibleApp`)
  - Tkinter interface
  - Queue polling system
  - Text rendering and layout

- **Service Layer** (`BibleService`)
  - Coordinates parsing and data retrieval
  - Handles validation and formatting

- **Repository Layer** (`BibleRepository`)
  - SQLite access
  - Verse queries and book lookup

- **Speech Layer** (`SpeechListener`)
  - Microphone streaming using `sounddevice`
  - Vosk speech recognition engine

- **Parser Layer**
  - Converts Ukrainian speech into:
    ```
    book → chapter → verse
    ```

- **Utilities**
  - Text fitting algorithm
  - Text sanitization
  - Number parsing (Ukrainian → integer)

---

## How It Works

1. The application captures audio from the microphone
2. Converts speech to text using **Vosk (offline ASR)**
3. Parses the spoken Bible reference
4. Queries the verse from the **local SQLite database**
5. GUI displays formatted result with adaptive font sizing

---

## Tech Stack

- **Python 3.10+**
- **Tkinter** — desktop GUI 
- **Vosk** — offline speech recognition
- **vosk-model-small-uk-v3** — Ukrainian language model
- **SQLite3** — local database for Bible verses
- **Standard Python libraries**

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/alexkanav/bible-voice-search
cd bible-voice-search
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
````

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Vosk model

Download and extract the Vosk Ukrainian model:
    
    vosk-model-small-uk-v3

Place it in the project directory (or update the model path in the code).

---

## Usage

Run the application:

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
- Ideal for privacy-focused users and environments with limited connectivity

---

## Possible Improvements

- Support for multiple Bible translations
- Advanced NLP parsing (ML model)
- Highlighting verse ranges
- Search mode (not only references)
- Support for additional languages
- Enhanced GUI styling

---

# License

MIT License — Free to use, modify, and distribute.