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

def parallel_ssh(ip_list,host_config,command_to_run,script_to_copy,username,password_initial):
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
def parallel_ssh_v2(ip_list,host_config,command_to_run):
    #Connect to the hosts and run commands
    client = ParallelSSHClient(ip_list, host_config=host_config,timeout=30,num_retries=1)
    ###Executing Command
    print("Executing command: "+command_to_run)
    output = client.run_command(command_to_run,stop_on_errors=False,sudo=True,use_pty=True)
    return_str=""

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
def cidr_to_ips(cidr):   
def checker(ip_list):

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
    command_to_run = "uname -a && whoami"
    username="kali"
    password_initial="kali"

    while (True):
        output=str(parallel_ssh(ip_list,host_config,command_to_run,script_to_copy,username,password_initial))
        time.sleep(3)
        return output
        
#To Compile using pyinstaller
#pyinstaller --hidden-import ssh2.agent --hidden-import ssh2.pkey --hidden-import ssh2.channel --hidden-import ssh2.sftp_handle --hidden-import ssh2.listener --hidden-import ssh2.statinfo --hidden-import ssh2.knownhost --hidden-import ssh2.fileinfo --hidden-import ssh2.publickey --onefile parallelssh_v11.py
#then staticx to make it statically linked