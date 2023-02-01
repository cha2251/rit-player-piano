# rit-player-piano

https://cha2251.github.io/rit-player-piano/

# Installing the correct verison of Python
- This project requires Python 3.8, as some of the required libraries aren't updated for the latest versions
- Linux installation:
    - `wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tar.xz`
    - `tar -xzvf Python-3.8.10.tar.xz && cd Python-3.8.10`
    - `./configure`
    - `make`
    - `make install`
- Windows installation:
    - Download the installer from `https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe`
    - Run the installer, making sure `Add Python 3.8 to PATH` is selected
    - Modify your PATH ordering or make a soft link so that you can run this specific version of Python

# Python Virtual Environment
- To keep package management and builds synced, use a python venv
- Make sure you create the venv using Python 3.8
- To create: 
    - `python3 -m venv venv`
- To activate:
    - On windows: `.\venv\Scripts\activate.bat`
    - On Linux: `source venv/Scripts/activate`
- To deactivate:
    - On windows: `.\venv\Scripts\deactivate.bat`
    - On Linux: Type Ctrl + D

# Running Locally
- Run with `python -m src.common.main` to prevent package errors

# Requirements
- If running Linux, install dependencies with `sudo apt-get install -y libasound2-dev pkg-config libjack-dev portaudio19-dev`
- Install packages with `pip install -r requirements.txt`
- Export current environment configuration file with `pip freeze > requirements.txt`
 - Make sure you install the existing packages first and you're in a venv before exporting!

# Running unit test
- Run tests with `pytest` in top level directory
- Follow test discovery syntax when creating new tests 
 - https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#test-discovery
 - Tip: to ensure print statements work in tests (if you need them) run `pytest -s`

# Building Executeable
- Start virtual environment
- Windows:
    - In top level directory run: `pyinstaller.exe src\common\main.py --clean --onefile --add-data=".\MIDI_Files\*;.\MIDI_Files\"`
        - Fix permission errors with: `chmod -R -c u+rwx .`
- Linux:
    - In top level directory run: `pyinstaller src\common\main.py --clean --onefile --add-data="/MIDI_Files/*:/MIDI_Files/"`
        - Fix permission errors with: `chmod -R -c u+rwx .`
