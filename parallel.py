from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig
import sys
import csv
from gevent import joinall


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

def parallel_ssh_v2(ip_list, host_configuration, command_to_run):
    # Connect to the hosts and run commands
    client = ParallelSSHClient(ip_list, host_config=host_configuration,timeout=10, num_retries=1)
    ###Executing Command
    print("Executing command: " + command_to_run)
    output = client.run_command(command_to_run, stop_on_errors=False, sudo=True, use_pty=True)
    #client.join(output)
    msg=""
    #print(output)
    #for value in range(len(host_config)):
      #  print("Host Config: "+str(host_configuration[value].user)+":"+str(host_configuration[value].password))
    print("Output: "+str(output))
    ##THE OUTPUT IS UNORDERED, FIX THIS
    for host_out in output:
        #Using the alias set on each host to get the correct credentials
        value = int(host_out.alias)
        try:
            #print("Writing to stdin: " + host_configuration[value].password + " for host: " + host_out.host)
            print(host_configuration[value].user+" "+host_configuration[value].password+" "+host_out.host)
            if host_out.stdin is not None:
                #Escalate to root if not already root
                if host_configuration[value].user!="root":
                    print("Escalating to sudo for user: " + host_configuration[value].user + " for host: " + host_out.host)
                    host_out.stdin.write(host_configuration[value].password + '\n')
                else:
                    print("User already root: " + host_configuration[value].user + " for host: " + host_out.host)
                    #host_out.stdin.write("censored" + '\n')
                host_out.stdin.flush()
                print("Host: " + host_out.host + " has been written to")
                if host_out.stdout:
                    print("Host: " + host_out.host + " has stdout")
                    stdout = list(host_out.stdout)
                    success_message = "✅[SUCCESS] Host %s: exit code %s, output %s\n" % (
                    host_out.host, host_out.exit_code, stdout)
                    msg=msg+success_message
            else:
                print("Exception: " + host_out.host+" "+str(host_out.exception))
                fail_message = "🛑[FAIL] Host %s: exception %s\n" % (
                host_out.host, host_out.exception)
                msg=msg+fail_message
        except Exception as e:
            print("Exception: "+str(e))
            fail_message = "🛑[FAIL] Host %s: exception %s\n" % (
                host_out.host, host_out.exception)
            msg=msg+fail_message
    return msg

##CHANGE THIS TO BE A LIST CONTAINING DICTIONARIES
def csv_to_dict(filename):
    result = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ip, user_pass = row[0], row[1]
            username, password = user_pass.split(':')
            result.append({ip: {'username': username, 'password': password}})
    return result

def checker(ip_list,command_to_run):
    ips_logins=csv_to_dict(ip_list)
    ips=[]
    host_config = []
    number_label=0
    for login in ips_logins:
        for ip, credentials in login.items():
            ips.append(ip)
            host_config.append(HostConfig(user=credentials['username'], password=credentials['password'],alias=str(number_label)))
            number_label=number_label+1
    output=str(parallel_ssh_v2(ips,host_config,command_to_run))
    #print(output)
    return output
        
#To Compile using pyinstaller
#pyinstaller --hidden-import ssh2.agent --hidden-import ssh2.pkey --hidden-import ssh2.channel --hidden-import ssh2.sftp_handle --hidden-import ssh2.listener --hidden-import ssh2.statinfo --hidden-import ssh2.knownhost --hidden-import ssh2.fileinfo --hidden-import ssh2.publickey --onefile parallelssh_v11.py
#then staticx to make it statically linked