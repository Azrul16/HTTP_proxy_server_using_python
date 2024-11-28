from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import time
import logging

CACHE = {}
RATE_LIMIT = {}
RATE_LIMIT_WINDOW = 10  # seconds
RATE_LIMIT_COUNT = 5  # max requests per window

logging.basicConfig(filename='proxy_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class ProxyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global CACHE, RATE_LIMIT

        client_ip = self.client_address[0]
        request_path = self.path

        # Rate Limiting
        current_time = time.time()
        if client_ip not in RATE_LIMIT:
            RATE_LIMIT[client_ip] = []
        RATE_LIMIT[client_ip] = [
            t for t in RATE_LIMIT[client_ip] if current_time - t < RATE_LIMIT_WINDOW
        ]
        if len(RATE_LIMIT[client_ip]) >= RATE_LIMIT_COUNT:
            self.send_response(429)
            self.end_headers()
            self.wfile.write(b"Rate limit exceeded. Try again later.")
            return
        RATE_LIMIT[client_ip].append(current_time)

        # Cache Check
        if request_path in CACHE:
            logging.info(f"Cache hit for {request_path}")
            self.send_response(200)
            server_socket.connect(("localhost", 8000))
            self.end_headers()
            self.wfile.write(CACHE[request_path])
            return

        # Forward Request to Main Server
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            request_line = f"GET {request_path} HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
            server_socket.send(request_line.encode())

            response = b""
            while chunk := server_socket.recv(4096):
                response += chunk

            CACHE[request_path] = response
            logging.info(f"Request for {request_path} forwarded to main server")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)
        except Exception as e:
            logging.error(f"Error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode())
        finally:
            server_socket.close()

def run_proxy():
    proxy_address = ("localhost", 8080)
    httpd = HTTPServer(proxy_address, ProxyRequestHandler)
    print("Proxy server running on http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run_proxy()
