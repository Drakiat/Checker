# Checker

Checker is an automated tool designed to monitor the persistence of compromised accounts and open ports on compromised machines over time during red team engagements.
<img width="771" alt="image" src="https://github.com/Drakiat/Checker/assets/70113570/6c3ec0b9-8460-4bbe-aee1-e7ab28ad60cb">


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

2. Create a `ip_file.txt` file to set the target ips to scan, which will continutly scanned for ports and output open ports. The format for this file should one ip per line:
   ```
   127.0.0.1
   192.168.1.1
   ```

3. Create a `web_file.txt` file to set the target URLs to scan, which will continutly scanned for 200 responses. The format for this file should one URL per line:
   ```
   https://google.com/
   https://bing.com/
   ```
4. Start the program:
   ```
   python3 main.py
   ```
Feel free to modify the variable in main.py according to your specific requirements.
