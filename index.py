from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

REPORTS = []

class handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def do_GET(self):
        if self.path.startswith("/api/health"):
            return self._send(200, {"ok": True, "service": "CleanTrust API", "mode": "demo"})
        if self.path.startswith("/api/reports"):
            return self._send(200, {"reports": REPORTS})
        return self._send(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/report":
            return self._send(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            report = {
                "id": len(REPORTS) + 1,
                "toilet_id": data.get("toilet_id"),
                "issue": data.get("issue", "Other"),
                "description": data.get("description", ""),
                "created_at": datetime.utcnow().isoformat() + "Z",
                "status": "pending"
            }
            REPORTS.append(report)
            return self._send(201, {"ok": True, "report": report})
        except Exception as exc:
            return self._send(400, {"ok": False, "error": str(exc)})
