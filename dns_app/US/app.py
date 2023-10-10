from flask import Flask, request, jsonify
import json
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Extract the parameters from the request
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Validate the parameters
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify(error="Bad request"), 400

    # Query the authoritative DNS server to get the IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        dns_query = f"TYPE A\nNAME {hostname}\n"
        s.sendto(dns_query.encode(), (as_ip, int(as_port)))
        
        # Wait for a response from AS
        data, addr = s.recvfrom(1024)
        response_lines = data.decode().split('\n')
        #print(f"response_lines:{response_lines}")
        for line in response_lines:
            if line.startswith("VALUE"):
                ip_address = line.split(' ')[1]
                break
        else:
            return jsonify(error="Failed to query for IP address"), 500

    # Construct the Fibonacci server URL
    fs_url = f"http://{ip_address}:{fs_port}/fibonacci?number={number}"

    # Query the Fibonacci server
    try:
        response = requests.get(fs_url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500
    
    parsed_response = json.loads(response.text)
    return jsonify(parsed_response), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)