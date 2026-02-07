import re
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

# Simple PII patterns for demonstration
PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b"
}

class PIIRedactor:
    def redact(self, text):
        redacted_text = text
        for label, pattern in PII_PATTERNS.items():
            redacted_text = re.sub(pattern, f"[{label}_REDACTED]", redacted_text)
        return redacted_text

class ProxyHandler(BaseHTTPRequestHandler):
    redactor = PIIRedactor()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Redact PII from the outgoing request
        redacted_data = self.redactor.redact(post_data)
        
        # Log the transaction (Audit Log)
        print(f"Original: {post_data}")
        print(f"Redacted: {redacted_data}")
        
        # Forward to the actual AI service (Mocked for now)
        # In a real scenario, this would forward to api.openai.com
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "success",
            "message": "Request processed and redacted",
            "redacted_content": redacted_data
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=ProxyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"PII Redaction Proxy running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
