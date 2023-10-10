from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

# Globals
AS_IP = None
AS_PORT = None
HOSTNAME = None

@app.route('/register', methods=['PUT'])
def register():
    global AS_IP, AS_PORT, HOSTNAME
    data = request.json
    HOSTNAME = data['hostname']
    AS_IP = data['as_ip']
    AS_PORT = data['as_port']
    
    # Create the DNS message
    dns_message = f"TYPE A\nNAME {HOSTNAME}\nVALUE {data['ip']}\n"
    
    # Send DNS message via UDP to AS
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(10)  # sets a 5-second timeout
        
        s.sendto(dns_message.encode(), (AS_IP, int(AS_PORT)))
    
        try:
            confirmation, _ = s.recvfrom(1024)
            
            if confirmation.decode() != "Registration Successful":
                raise Exception("Registration failed on AS")
            else:
                print(f"confirmation!:{confirmation}")
                # Return 201 status code
                return '', 201

        except socket.timeout:
            # Handle the timeout scenario. Maybe log an error or retry.
            return jsonify(error="socket.timeout"), 408
     
    
    
    

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Use a UDP connection to an arbitrary public address to determine the most appropriate network interface for outbound connections.
    # This does not actually establish a connection.
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        x = int(number)
        result = calculate_fib(x)
        return jsonify(result=result), 200
    except ValueError:
        return jsonify(error="Invalid number format"), 400

def calculate_fib(n):
    # Simple Fibonacci calculation
    if n <= 1:
        return n
    else:
        return calculate_fib(n-1) + calculate_fib(n-2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)