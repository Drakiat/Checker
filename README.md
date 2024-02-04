# RedTeam-Checker

RedTeam-Checker is an automated tool designed to monitor the persistence of backdoors and default settings on compromised machines over time.

## Compatibility
This tool is built to support Python 3.10. Please note that Python versions 3.11 and higher are not compatible with the parallel-ssh library.

## Installation
To install the required dependencies, use the following command:
```bash
pip install -r requirements.txt
```

## Setup
1. Create a `logins.csv` file to specify the targets. The format for the file should be:
   ```
   ip,username:password
   ```

2. Create a `scoring.csv` file to set the target scoring. The format for this file should be:
   ```
   ip,port
   ```

Feel free to customize the files according to your specific requirements. Happy checking!