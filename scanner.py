import nmap
nm = nmap.PortScanner()
nm.scan(hosts='192.168.2.0/24', arguments='-n -sP -PE -PA21,23,80,3389 --min-rate 4500 --max-rtt-timeout 1500ms')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
	print('{0}:{1}'.host)
