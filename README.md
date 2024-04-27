<div class="readme-header" align="center">
  <img src="https://github.com/ussaka/todoist-prioritizer/blob/main/docs/priority.svg" alt="Description of the image" width="150" height="150">
  <h1>todoist-prioritizer</h1>  

  [![Release](https://img.shields.io/badge/Release-1.0.0-blue?style=flat)](https://github.com/ussaka/todoist-prioritizer/releases/latest)
  [![wakatime](https://wakatime.com/badge/user/41c5948e-4207-46a3-bcb4-2f355d15e4ac/project/018e4894-c1f1-49df-b86c-1d01599a769f.svg)](https://wakatime.com/badge/user/41c5948e-4207-46a3-bcb4-2f355d15e4ac/project/018e4894-c1f1-49df-b86c-1d01599a769f.svg)
  [![CodeQL](https://github.com/ussaka/todoist-prioritizer/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ussaka/todoist-prioritizer/actions/workflows/github-code-scanning/codeql)
  <p>
      <b>
          📑 <a href="https://ussaka.github.io/todoist-prioritizer/">Documentation</a>
      </b>
  </p>  
  <h3>Automatic <a href="https://todoist.com">Todoist</a> tasks prioritizer</h3>
</div>

# Description
The todoist-prioritizer is a Python script designed to manage Todoist tasks priority levels. Users can determine the number of tasks they want at each priority level, ranging from P1 (highest priority) to P3 (lowest priority). This tool is best suited for users with large amount of tasks without `due date`.

### How it works?
- Specify the number of tasks desired for each priority level (P1 to P3)
- When task count at specific priority level falls below the user's preferences, the script automatically promotes tasks from lower priority levels to higher ones, starting from the oldest task
  - E.g. If P1 level has 3/5 tasks then promote tasks from P2 to P1 starting from the oldest task in P2. After that, if P2 has less tasks than desired promote tasks from P3 to it and so on... 
- The script runs once a day at a time specified by the user

# Usage
If the script is run without arguments, it will prompt for user input. Only Todoist api token needs to be set, the user can run other settings with default values. The api token is available at [integrations/developer](https://todoist.com/prefs/integrations).

Available commands
```bash
todoist-prioritizer --help
usage: todoist-prioritizer.py [-h] [-a API_TOKEN] [-p1 P1_SIZE] [-p2 P2_SIZE] [-p3 P3_SIZE] [-hh RUN_HOUR]
                              [-mm RUN_MINUTE] [-r] [-d]

options:
  -h, --help                     show this help message and exit
  -a API_TOKEN, --api API_TOKEN  Set api token
  -p1 P1_SIZE                    Maximum number of P1 tasks
  -p2 P2_SIZE                    Maximum number of P2 tasks
  -p3 P3_SIZE                    Maximum number of P3 tasks
  -hh RUN_HOUR                   The hour to run the script, 24 hour format
  -mm RUN_MINUTE                 The minute to run the script, 24 hour format
  -r, --reset                    Reset configuration to default values
  -d, --debug                    Enable debug logging level
```

Example usage  
- Windows
  ```bash
  ./todoist-prioritizer.exe -a 3x4mpl34p1k3y -h 00 -m 00 -d
  ```
- Python
  ```bash
  python todoist-prioritizer.py -a 3x4mpl34p1k3y -h 00 -m 00 -d
  ```

[Default settings](https://github.com/ussaka/todoist-prioritizer/blob/main/src/config.ini#L1)

# Installation
Pre-compiled .exe binaries are [released](https://github.com/ussaka/todoist-prioritizer/releases/latest) for Windows users.

### Python
Install dependencies
```bash
pip install -r requirements.txt
```

### PyInstaller
Users can compile the script by themselves to an executable using [PyInstaller](https://pyinstaller.org).
```bash
pyinstaller src/todoist-prioritizer.py --icon=docs/priority.ico -c --onefile --add-data src/config.ini:.
```
