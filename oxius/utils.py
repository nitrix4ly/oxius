def build_headers(method, host, path, default_headers, custom_headers=None, body=None):
    request_line = f"{method} {path} HTTP/1.1\r\n"
    merged_headers = default_headers.copy()

    if custom_headers:
        for key, value in custom_headers.items():
            merged_headers[key.title()] = value

    merged_headers["Host"] = host
    merged_headers.setdefault("Connection", "close")

    if body:
        merged_headers.setdefault("Content-Type", "application/json")
        merged_headers["Content-Length"] = str(len(body))

    header_lines = "".join(f"{key}: {value}\r\n" for key, value in merged_headers.items())
    return request_line + header_lines + "\r\n"
