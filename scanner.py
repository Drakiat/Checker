import nmap

def scan_ips(ip_addresses, ports):
    nm = nmap.PortScanner()
    open_ports = {}
    # Convert list of IP addresses to a comma-separated string
    ip_addresses_str = " ".join(ip_addresses)
    ports_str = ','.join([str(i) for i in ports])
    res = nm.scan(ip_addresses_str, arguments='-Pn -p {0} --min-rate 4500 --max-rtt-timeout 1500ms --open'.format(ports_str),timeout=60)
    for ip in res['scan']:
        open_ports[ip] = []
        for port in res['scan'][ip]['tcp']:
            if res['scan'][ip]['tcp'][port]['state'] == 'open':
                open_ports[ip].append(port)
    for ip in ip_addresses:
        if ip not in open_ports.keys():
            open_ports[ip]=["No open ports found."]
    return open_ports
