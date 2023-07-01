import psutil

def get_used_ports():
    connections = psutil.net_connections()
    used_ports = set()
    for conn in connections:
        if conn.status == 'LISTEN':
            used_ports.add(conn.laddr.port)
    return used_ports

# Get a set of used ports
used_ports = get_used_ports()
print(used_ports)
