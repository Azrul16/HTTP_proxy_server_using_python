import requests

def main():
    proxies = {
        "http": "http://localhost:8080",
        "https": "http://localhost:8080"
    }
    try:
        response = requests.get("http://example.com", proxies=proxies)
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()