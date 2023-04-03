import sys
import os
import requests

def send_file(file_path, url):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Response received:")
        print(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python send_file.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    url = 'http://localhost:8000'  # Change this to the server URL where you want to send the file
    send_file(file_path, url)
