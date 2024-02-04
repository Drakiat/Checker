import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import time
import parallel
import scanner
import csv
import datetime

##Config files
scoring_file = 'scoring.csv'
login_file = 'logins.csv'
#Sleep time for the port scanner and ssh in seconds
scan_sleep = 20
ssh_sleep = 10


root = tk.Tk()
root.title("Red Team Checker GUI")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)


tabControl.add(tab1, text ='Default Credentials')
tabControl.add(tab2, text ='Open Ports')


tabControl.pack(expand = 1, fill ="both")

ttk.Label(tab1, text="Default Credentials").grid(column=0, row=0, padx=30, pady=30)
ttk.Label(tab2, text="Open Ports").grid(column=0, row=0, padx=30, pady=30)

# Add a read-only text box to tab1
text_box1 = scrolledtext.ScrolledText(tab1)
text_box1.grid(column=0, row=1, padx=30, pady=30, sticky="nsew")
text_box1.configure(state ='disabled') # Make it read-only

# Add a read-only text box to tab2
text_box2 = scrolledtext.ScrolledText(tab2)
text_box2.grid(column=0, row=1, padx=30, pady=30, sticky="nsew")
text_box2.configure(state ='disabled') # Make it read-only

# Configure the row containing the text boxes to expand with the window
tab1.grid_rowconfigure(1, weight=1)
tab1.grid_columnconfigure(0, weight=1)
tab2.grid_rowconfigure(1, weight=1)
tab2.grid_columnconfigure(0, weight=1)
#configure colors
text_box1.tag_config('red', foreground='red')
text_box1.tag_config('green', foreground='green')
text_box2.tag_config('red', foreground='red')
text_box2.tag_config('green', foreground='green')

#Parse csv to make dictionnaries
def csv_to_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            key = row[0]
            value = str(row[1])
            dictionary[key] = dictionary[key]+","+value if key in dictionary else value
    return dictionary


def pssh():
    """
    Function to start parallel SSH and display the output in a text box.

    This function starts the parallel SSH process, retrieves its output,
    and updates a text box with the output. The output is color-coded based
    on the presence of the word "FAIL" in each item of the output.

    Args:
        None

    Returns:
        None
    """
    while True:
        # Start scan 
        text_box1.configure(state='normal')
        text_box1.insert('end', "Starting parallel SSH at " + str(datetime.datetime.now()) + "\n")
        text_box1.configure(state='disabled')
        text_box1.see('end')
        # Call the parallel_ssh function and get its output
        output1 = parallel.checker(login_file)
        output1_list = output1.split('\n')
        for item in output1_list:
            if "FAIL" in item:
                tag = 'red'
            else:
                tag = 'green'
            # Update text_box1 with each item of the list
            text_box1.configure(state='normal')
            text_box1.insert('end', item + '\n', tag)
            text_box1.configure(state='disabled')  
            text_box1.see('end')
        time.sleep(ssh_sleep)
##Port Scanner
def PortScanner():
    """
    This function performs port scanning on a set of IP addresses and ports.
    It retrieves the IP addresses and ports from a scoring file and scans them using a scanner object.
    The results are displayed in a text box.
    """
    # Rest of the code...
def PortScanner():
    #This is the dictionary that will be used to store the ips and ports that are scored
    #scored={"192.168.2.19":[22,80],"192.168.2.1":[22,80]}
    scored=csv_to_dictionary(scoring_file)
#This is gross but it works ipset(set) and ports(string) are used to store the ips and ports to scan
    ports=''
    ipset=set()
    portset=set()
    for key in scored.keys():
        ipset.add(key)
        portset.add(str(scored[key]))
    for item in portset:
        ports+=str(item)+','
    ports=str(ports[:-1])
#main loop
    while True:
        #Start scan 
        text_box2.configure(state='normal')
        text_box2.insert('end',"Starting scan at "+str(datetime.datetime.now())+"\n")
        text_box2.configure(state='disabled')
        text_box2.see('end')
        nm=scanner.scan_ips(ipset,ports)
        for key in nm:
            #check if the key is in the scored dictionary
            key_checked=key.split(",")[0]
            if key_checked in scored.keys():
                value_checked=int(key.split(",")[1])
                if str(value_checked) in scored[key_checked].split(","):
                    #Print text
                    if nm[key] == "open":
                        tag = 'green'
                    else:
                        tag = 'red'
                    text_box2.configure(state='normal')
                    text_box2.insert('end', key + ' ' + nm[key] + '\n', tag)
                    text_box2.configure(state='disabled')
                    text_box2.see('end')
            else:
                print("Key not found")
                continue
        ##Sleep for 20 seconds
        text_box2.configure(state='normal')
        text_box2.insert('end',"Sleeping for "+str(scan_sleep)+" seconds\n")
        text_box2.configure(state='disabled')
        text_box2.see('end')
        time.sleep(scan_sleep)

# Start a new thread that updates the text boxes every 10 seconds

threading.Thread(target=pssh, daemon=True).start()
threading.Thread(target=PortScanner, daemon=True).start()


# Start a new thread that updates the text boxes every 10 seconds

root.mainloop()
