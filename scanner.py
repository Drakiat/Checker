import nmap

def scan_ips(ip_addresses, ports):
    nm = nmap.PortScanner()
    open_ports = {}
    # Convert list of IP addresses to a comma-separated string
    ip_addresses_str = " ".join(ip_addresses)
    res = nm.scan(ip_addresses_str, arguments='-F -n --min-rate 4500 --max-rtt-timeout 1500ms --open',timeout=60)
    print(res)
    for ip in res['scan']:
        open_ports[ip] = []
        for port in res['scan'][ip]['tcp']:
            if res['scan'][ip]['tcp'][port]['state'] == 'open':
                open_ports[ip].append(port)
    return open_ports
