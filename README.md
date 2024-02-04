# RedTeam-Checker

RedTeam-Checker is an automated tool designed to monitor the persistence of backdoors and default settings on compromised machines over time.

## Compatibility
This tool is built to support Python 3.10. Please note that Python versions 3.11 and higher are not supported and might not be compatible with the parallel-ssh library.
## Installation
To install the required dependencies, use the following command(it is higly recommended to use a virtual environment such as [venv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)):
```bash
pip install -r requirements.txt
```

## Setup
1. Create a `logins.csv` file to specify the targets for the Parallel-SSH function which will attempt to log in to the targets using the supplied credentials. The format for the file should be:
   ```
   ip,username:password
   ```

2. Create a `scoring.csv` file to set the target scoring, which will continutly scan for ports and check their state using nmap. The format for this file should be:
   ```
   ip,port
   ```
3. Start the program:
   ```
   python3 main.py
   ```
Feel free to customize the files according to your specific requirements.