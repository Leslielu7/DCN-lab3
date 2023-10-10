import socket

DNS_DB_FILE = '/var/lib/address_server/dns_db.txt'

def register_domain(data):
    with open(DNS_DB_FILE, 'a') as f:
        f.write(data)

def query_domain(name):
    with open(DNS_DB_FILE, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            if lines[i+1].strip() == f"NAME {name}" and lines[i].strip() == "TYPE A":
                return lines[i+2].strip().split(' ')[1]  # Return IP
    return None

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    ttl_value = 10 
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl_value)
    s.bind(('0.0.0.0', 53533))
    print("AS is running and listening on port 53533...")
    while True:
        data, addr = s.recvfrom(1024)
       
        lines = data.decode().split('\n')
      
        if len(lines) == 4:  # Registration
            register_domain(data.decode())
            
            confirmation_message = "Registration Successful"
            s.sendto(confirmation_message.encode(), addr)
    
        else:  # DNS Query
            
            ip = query_domain(lines[1].split(' ')[1])
           
            if ip:
                response = f"TYPE A\n{lines[1]}\nVALUE {ip}\nTTL 10\n"
                s.sendto(response.encode(), addr)