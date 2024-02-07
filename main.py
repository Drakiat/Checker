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
ip_file = 'ip_file.txt'
login_file = 'logins.csv'
command_to_run = "id && hostname"
#Sleep time for the port scanner and ssh in seconds
scan_sleep = 20
ssh_sleep = 10
#List of ports to scan, this is the nmap list of top 1000 ports
ports=[80,23,443,21,22,25,3389,110,445,139,143,53,135,3306,8080,1723,111,995,993,5900,1025,587,8888,199,1720,465,548,113,81,6001,10000,514,5060,179,1026,2000,8443,8000,32768,554,26,1433,49152,2001,515,8008,49154,1027,5666,646,5000,5631,631,49153,8081,2049,88,79,5800,106,2121,1110,49155,6000,513,990,5357,427,49156,543,544,5101,144,7,389,8009,3128,444,9999,5009,7070,5190,3000,5432,1900]
print("Number of ports set to scan: ",len(ports))

# Create the main window
root = tk.Tk()
root.title("Checker GUI by wyldgoat")

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



# Add a check button to tab1
enabled_check_pssh = tk.BooleanVar(value=True)
enabled_checkbutton1 = ttk.Checkbutton(tab1, text="Enable", variable=enabled_check_pssh)
enabled_checkbutton1.grid(column=1, row=1, padx=10, pady=10)
# Add a check button to tab2
enabled_check_scanner = tk.BooleanVar(value=True)
enabled_checkbutton2 = ttk.Checkbutton(tab2, text="Enable", variable=enabled_check_scanner)
enabled_checkbutton2.grid(column=1, row=1, padx=10, pady=10)
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
text_box2.tag_config('blue', foreground='blue')
text_box2.tag_config('gold', foreground='gold2')
text_box2.tag_config('RoyalBlue', foreground='RoyalBlue3')

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
    while True:
        if enabled_check_pssh.get()==True:
            # Start scan 
            text_box1.configure(state='normal')
            text_box1.insert('end', "Starting parallel SSH at " + str(datetime.datetime.now()) + "\n")
            text_box1.configure(state='disabled')
            text_box1.see('end')
            # Call the parallel_ssh function and get its output
            output1 = parallel.checker(login_file,command_to_run)
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
            #sleep for configured seconds
            text_box1.configure(state='normal')
            text_box1.insert('end', "Sleeping for " +str(ssh_sleep) +" seconds\n")
            text_box1.configure(state='disabled')
            text_box1.see('end')
            time.sleep(ssh_sleep)
##Port Scanner
def PortScanner():
    
    #This is the dictionary that will be used to store the ips and ports that are scored
    #scored={"192.168.2.19":[22,80],"192.168.2.1":[22,80]}
#This is gross but it works ipset(set) and ports(string) are used to store the ips and ports to scan
    with open(ip_file) as f:
        ips = f.read().splitlines()
#main loop
    while True:
        if enabled_check_scanner.get()==True:
            #Show date
            text_box2.configure(state='normal')
            text_box2.insert('end',"Starting scan at "+str(datetime.datetime.now())+"\n")
            text_box2.configure(state='disabled')
            text_box2.see('end')
            #Start Scan
            nm=scanner.scan_ips(ips,ports)
            i=0
            for key in nm.keys():
                #check if the key is in the scored dictionary
                if key in ips:
                    text_box2.configure(state='normal')
                    text_box2.insert('end',key,'RoyalBlue')
                    text_box2.insert('end',":")
                    if nm[key]==["No open ports found."]:
                        text_box2.insert('end'," No open ports found.\n",'red')
                    else:
                        text_box2.insert('end',str(nm[key])+"\n",'gold')
                    text_box2.configure(state='disabled')
                    text_box2.see('end')
                    i=i+1
            ##Sleep for 20 seconds
            text_box2.configure(state='normal')
            text_box2.insert('end',"Sleeping for "+str(scan_sleep)+" seconds\n")
            text_box2.configure(state='disabled')
            text_box2.see('end')
            time.sleep(scan_sleep)

# Start a new thread that updates the text boxes every 10 seconds

#threading.Thread(target=pssh, daemon=True).start()
#threading.Thread(target=PortScanner, daemon=True).start()
pssh_thread=threading.Thread(target=pssh, daemon=True).start()
PortScanner_thread=threading.Thread(target=PortScanner, daemon=True).start()
# Start a new thread that updates the text boxes every 10 seconds

root.mainloop()
