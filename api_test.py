import subprocess
import json

def curl_request(url):
    try:
        # Wykonanie polecenia curl
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        # Konwersja odpowiedzi na JSON
        response_json = json.loads(result.stdout)
        return response_json
    except json.JSONDecodeError:
        print(f"Nieprawidłowa odpowiedź JSON dla URL: {url}")
        return None

def check_http_status(url):
    # Sprawdzanie statusu HTTP
    result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], capture_output=True, text=True)
    http_status = result.stdout.strip()
    return http_status == '200'

def test_endpoint(url, key_check):
    if not check_http_status(url):
        print(f"Test FAILED dla endpointu: {url} - Otrzymano niepoprawny HTTP status")
        return False

    response = curl_request(url)
    if response is None:
        print(f"Test FAILED dla endpointu: {url} - Nieprawidłowa odpowiedź JSON")
        return False

    if isinstance(response, list):
        response = response[0]

    if all(key in response for key in key_check):
        print(f"Test PASSED dla endpointu: {url}")
        return True
    else:
        print(f"Test FAILED dla endpointu: {url} - Brak kluczowych elementów {key_check}")
        return False

def test_api():
    endpoints = [
        ("https://jsonplaceholder.typicode.com/posts", ["userId", "id", "title"]),
        ("https://jsonplaceholder.typicode.com/posts/1", ["userId", "id", "title"]),
        ("https://jsonplaceholder.typicode.com/users", ["id", "name", "username"])
    ]

    for idx, (endpoint, keys) in enumerate(endpoints, 1):
        print(f"Test {idx}: {'PASSED' if test_endpoint(endpoint, keys) else 'FAILED'}")

if __name__ == "__main__":
    test_api()
