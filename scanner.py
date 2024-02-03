import nmap

def scan_ips(ips, ports):
	nm = nmap.PortScanner()
	results = {}
	
	for ip in ips:
		nm.scan(ip, arguments='-p {0} --min-rate 4500 --max-rtt-timeout 1500ms'.format(ports))
		for host in nm.all_hosts():
			for port in nm[host]['tcp']:
				status = nm[host]['tcp'][port]['state']
				key = f"{host},{port}"
				results[key] = status
	
	return results

#ips = ['192.168.2.19', '192.168.2.1', '192.168.2.21']
#ports = '21,22,80,443,3389'
#results = scan_ips(ips, ports)
#print(results)
