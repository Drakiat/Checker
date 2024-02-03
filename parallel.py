from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig
import sys
import os
import subprocess
import socket
import time
from gevent import joinall
from concurrent.futures import ThreadPoolExecutor


#variables

ip_list = []
subnet=""
username=""
password_initial=""
password_changed=""
command_to_run="pwd"
host_config = []
host_config_creds = []
script_to_copy=""

#check if on windows or linux
if sys.platform.startswith('win'):
    print('Running on Windows')
    running_windows=True
else:
    print('Running on Unix-like system')
    running_windows=False

#function to change cidr range to ip list
def cidr_to_ips(cidr):
    net, mask = cidr.split('/')
    mask = int(mask)
    net = list(map(int, net.split('.')))
    net_int = (net[0] << 24) + (net[1] << 16) + (net[2] << 8) + net[3]
    mask_int = (0xffffffff << (32 - mask)) & 0xffffffff
    ips = [f'{(net_int + i >> 24) & 0xff}.{(net_int + i >> 16) & 0xff}.{(net_int + i >> 8) & 0xff}.{(net_int + i) & 0xff}' for i in range(0, 2**(32-mask)-1)]
    return ips


def check_port_22(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((ip, 22))
    sock.close()
    if result == 0:
        return ip
    return None
#Function to read from file if it exists
def read_ssh_ips():
    file_path = "ssh_ips.txt"
    if os.path.isfile(file_path):
        #answer = input("File ssh_ips.txt found! Do you want to import IPs from ssh_ips.txt? (y/n) ").lower()
        if True:
            pass
        else:
            os.remove(file_path)
            return []
        with open(file_path, "r") as f:
            ips = [line.strip() for line in f.readlines()]
        return ips
    else:
        print(f"File {file_path} does not exist")
        return []


def parallel_ssh(ip_list,host_config,command_to_run,script_to_copy,username,password_initial):
    print("[*]Starting SSH connections...")
    print("The following hosts have been added to Parallel SSH: ")
    print(ip_list)
    print(" ")
    #Connect to the hosts and run commands
    if len(host_config)==0:
        client = ParallelSSHClient(ip_list,user=username,password=password_initial,timeout=30,num_retries=1)
    else:
        client = ParallelSSHClient(ip_list, host_config=host_config,timeout=30,num_retries=1)
    ###SCP file if sending script to all hosts
    if len(script_to_copy)!=0:
        print("Copying file: "+script_to_copy)
        cmds = client.scp_send(script_to_copy,"/tmp/"+script_to_copy)
        joinall(cmds, raise_error=False)
    ###Executing Command
    print("Executing command: "+command_to_run)
    output = client.run_command(command_to_run,stop_on_errors=False,sudo=True,use_pty=True)
    return_str=""
    ###Case 1:Using same creds for all hosts
    if len(password_initial)!=0:
        for host_out in output:
            try:
                host_out.stdin.write(password_initial+'\n')
                host_out.stdin.flush()
                hostname = host_out.host
                stdout = list(host_out.stdout)
                output_str = "[SUCCESS]"+"Host %s: exit code %s, output %s" % (
                    hostname, host_out.exit_code, stdout)
                print(output_str)
                return_str=return_str+output_str+"\n"
            except Exception:
                output_str = "[FAIL]"+"Host %s: exception %s" % (
                    host_out.host, host_out.exception)
                print(output_str)
                return_str=return_str+output_str+"\n"
        return return_str
        #Uncomment this to debug!!! 
#print(output)
    else:
###Case 2:Using different creds for all hosts
        value=0
        for host_out in output:
            try:
                host_out.stdin.write(host_config_creds[value]+'\n')
                host_out.stdin.flush()
                value=value+1
            except Exception:
                value=value+1
        for host_output in output:
            hostname = host_output.host
            try:
                stdout = list(host_output.stdout)
                return str("[SUCCESS]"+"Host %s: exit code %s, output %s" % (
                    hostname, host_output.exit_code, stdout))
            except Exception:
                return str("[FAIL]"+"Host %s: exception %s" % (
                    host_output.host, host_output.exception))
                
def main():     
    #print("Starting ping sweep...")
    #pingSweep()
    #print("Ping sweep complete! The following hosts have been added to Parallel SSH: ")
    script_to_copy=""
    ip_list=read_ssh_ips()
    if len(ip_list)==0:
        subnet=input("Input CIDR subnet: ")
        subnet_ips=cidr_to_ips(subnet)
        print("Starting SSH sweep...")
        ip_list=scan_ips(subnet_ips)
        file_path="ssh_ips.txt"
        if not os.path.exists(file_path):
            open(file_path, "w").close()
        with open(file_path, "a") as f:
            for item in ip_list:
                f.write(item + "\n")
        print("SSH sweep complete!")
        print(ip_list)
        print("")
        print("You may quit this script now and modify "+file_path+" if any hosts need to be added/excluded.")

    print("")
    print("")

    print("Do you want to: ")
    print("(1)Change a user's password")
    print("(2)Run a command on every host")
    print("(3)Run a local script on every host")
    answer1 = input("(1/2/3)")
    if answer1=='1':
        pass
    if answer1=='2':
        command_to_run = input("Command: ")
    if answer1=='3':
        script_to_copy=input("Script local path:")
        command_to_run ='set -m; chmod +x /tmp/'+script_to_copy+'; sleep 1; nohup /tmp/'+script_to_copy+' >/dev/null 2>&1 &'
    answer2 = input("Do you want to use different credentials for each host? (y/n) ").lower()
    if answer2 == "y":
        print("OK!")
        specific_creds(ip_list)
        username=""
        password_initial=""
    else:
        if answer1=='1':
            username=input("Username: ")
            password_initial=input('Old Password: ')
            password_changed=input('New Password: ')
            command_to_run='echo root:'+password_changed+' | chpasswd'
        else:
            username=input("Username: ")
            password_initial=input('Password: ')
    while (True):
        parallel_ssh(ip_list,host_config,command_to_run,script_to_copy,username,password_initial)
        time.sleep(15)
#main()
def checker():
    #print("Starting ping sweep...")
    #pingSweep()
    #print("Ping sweep complete! The following hosts have been added to Parallel SSH: ")
    script_to_copy=""
    ip_list=read_ssh_ips()
    if len(ip_list)==0:
        subnet=input("Input CIDR subnet: ")
        subnet_ips=cidr_to_ips(subnet)
        print("Starting SSH sweep...")
        file_path="ssh_ips.txt"
        if not os.path.exists(file_path):
            open(file_path, "w").close()
        with open(file_path, "a") as f:
            for item in ip_list:
                f.write(item + "\n")
        print("SSH sweep complete!")
        print(ip_list)
        print("")
        print("You may quit this script now and modify "+file_path+" if any hosts need to be added/excluded.")
   # answer1 = input("(1/2/3)")
    #if answer1=='1':
     #   pass
    if True:
        command_to_run = "uname -a && whoami"
    #if answer1=='3':
     #   script_to_copy=input("Script local path:")
     #   command_to_run ='set -m; chmod +x /tmp/'+script_to_copy+'; sleep 1; nohup /tmp/'+script_to_copy+' >/dev/null 2>&1 &'
    #answer2 = input("Do you want to use different credentials for each host? (y/n) ").lower()
    #if answer2 == "y":
    #    print("OK!")
    #    specific_creds(ip_list)
    #    username=""
    #    password_initial=""
    #else:
     #   if answer1=='1':
    username="kali"
    password_initial="kali"
    #password_changed=input('New Password: ')
    #command_to_run='echo root:'+password_changed+' | chpasswd'
    while (True):
        time.sleep(3)
        output=str(parallel_ssh(ip_list,host_config,command_to_run,script_to_copy,username,password_initial))
        time.sleep(3)
        return output
        
#To Compile using pyinstaller
#pyinstaller --hidden-import ssh2.agent --hidden-import ssh2.pkey --hidden-import ssh2.channel --hidden-import ssh2.sftp_handle --hidden-import ssh2.listener --hidden-import ssh2.statinfo --hidden-import ssh2.knownhost --hidden-import ssh2.fileinfo --hidden-import ssh2.publickey --onefile parallelssh_v11.py
#then staticx to make it statically linked