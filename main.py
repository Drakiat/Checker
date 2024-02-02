import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import time
import parallel
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

def update_text_boxes():
    while True:
        text_box1.configure(state ='normal')
        text_box1.insert('end', 'Message 1\n','red')
        text_box1.configure(state ='disabled')

        text_box2.configure(state ='normal')
        text_box2.insert('end', 'Message 2\n','blue')
        text_box2.configure(state ='disabled')
        # Configure the tags
        text_box1.tag_config('red', foreground='red')
        text_box2.tag_config('blue', foreground='blue')  
        time.sleep(1)

#Please comlpete the function below to call a function from another file that will continuously update the text boxes with the output of the parallel_ssh function
#This function should be called in a new thread so that the GUI remains responsive and will continuously update the text boxes with the output of the parallel_ssh function
def pssh():
    while True:
        # Call the parallel_ssh function and get its output
        output1 = parallel.checker()
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

        # Configure the tags
        text_box1.tag_config('red', foreground='red')
        text_box1.tag_config('green', foreground='green')  

        time.sleep(1)

# Start a new thread that updates the text boxes every 10 seconds
threading.Thread(target=pssh, daemon=True).start()


# Start a new thread that updates the text boxes every 10 seconds
#threading.Thread(target=update_text_boxes, daemon=True).start()

root.mainloop()
