import json

class Response:
    def __init__(self, raw_data):
        header_data, body = raw_data.split(b"\r\n\r\n", 1)
        try:
            self.body = body.decode("utf-8")
        except UnicodeDecodeError:
            self.body = body.decode("utf-8", errors="replace")

        lines = header_data.decode("utf-8").splitlines()
        self.status = int(lines[0].split()[1])
        self.headers = {}

        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                self.headers[key.lower()] = value

    def text(self):
        return self.body

    def json(self):
        content = self.body.strip()
        if content.startswith("<!DOCTYPE html>") or "<html" in content.lower():
            return {
                "type": "error",
                "message": "Received HTML instead of JSON",
                "raw": content[:300]
            }
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "type": "error",
                "message": "Invalid JSON response",
                "raw": content[:300]
            }
        
