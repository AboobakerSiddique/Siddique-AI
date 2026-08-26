import httpx

def local_iot_request(ip_address: str, endpoint: str = "/", method: str = "GET", payload: dict = None) -> str:
    """Sends an HTTP request to a local network device (like an ESP32, Raspberry Pi, or sensor node).
    Args:
        ip_address: The local IP of the microcontroller (e.g., '192.168.1.100').
        endpoint: The API endpoint on the device (e.g., '/status', '/read_gas').
        method: 'GET' or 'POST'.
        payload: Optional JSON dictionary for POST requests.
    """
    # Clean up formatting
    ip_address = ip_address.replace("http://", "").replace("https://", "").strip('/')
    endpoint = endpoint.lstrip('/')
    url = f"http://{ip_address}/{endpoint}"
    
    try:
        with httpx.Client(timeout=5.0) as client:
            if method.upper() == "POST":
                resp = client.post(url, json=payload or {})
            else:
                resp = client.get(url)
            resp.raise_for_status()
            return f"Device Response ({resp.status_code}): {resp.text}"
    except httpx.TimeoutException:
        return f"Error: Connection to {url} timed out. Device might be offline."
    except Exception as e:
        return f"Error connecting to {url}: {str(e)}"
