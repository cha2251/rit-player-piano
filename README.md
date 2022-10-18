# rit-player-piano

https://cha2251.github.io/rit-player-piano/

# Python Virtual Environment
- To keep package management and builds synced, use a python venv
- To create: 
    - python3 -m venv venv
- To activate:
    - On windows: .\venv\Scripts\activate.bat
    - On Linux: source venv/bin/activate
- To deactivate:
    - On windows: .\venv\Scripts\deactivate.bat
    - On Linux: Ctrl + D

# Requirements
- Install packages with `pip install -r requirements.txt`
- Export current environment configuration file with `pip freeze > requirements.txt`

# Running unit test
- Run tests with `pytest` in top level directory
- Follow test discovery syntax when creating new tests 
 - https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#test-discovery