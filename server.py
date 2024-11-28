from http.server import SimpleHTTPRequestHandler, HTTPServer

class MainServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Hello! You requested: {self.path}".encode())

def run_server():
    server_address = ("localhost", 8000)
    httpd = HTTPServer(server_address, MainServerHandler)
    print("Main server running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
