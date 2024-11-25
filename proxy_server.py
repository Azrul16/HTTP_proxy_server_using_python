from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import logging

# Set up logging
logging.basicConfig(filename='proxy_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class ProxyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        logging.info(f"Client: {self.client_address[0]} - Requested server: {url}")
        try:
            example_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            example_socket.connect(("localhost", 8000))
            request = f"GET {url} HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
            example_socket.send(request.encode())
            response = b""
            while True:
                chunk = example_socket.recv(4096)
                if not chunk:
                    break
                response += chunk
            self.send_response(200)
            self.send_header("Content-Length", len(response))
            self.end_headers()
            self.wfile.write(response)
            logging.info(f"Proxy connected to example server: {self.client_address[0]} - Connected to example server")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            example_socket.close()

def run_server():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, ProxyRequestHandler)
    print("Proxy server started on port 8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()