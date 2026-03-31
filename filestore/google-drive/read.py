import hex
import requests

# 1. Gather context from Hex
access_token = hex.get_state("access_token")
base_path = hex.get_state("base_path")  # Assuming this is a folder ID
filename = hex.get_input("filename")

# 2. Perform the logic
headers = {
    "Authorization": f"Bearer {access_token}",
}

# Search for the file by name (and optionally in a specific folder)
url = "https://www.googleapis.com/drive/v3/files"
q = f"name = '{filename}'"
# if base_path:
#     q += f" and '{base_path}' in parents"

params = {
    "q": q,
    "fields": "files(id, name, mimeType)",
}

try:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Drive API search failed: {response.text}")
        hex.set_output("content", "")
        exit(1)

    files = response.json().get("files", [])
    if not files:
        print(f"File '{filename}' not found on Google Drive.")
        hex.set_output("content", "")
        exit(0)

    # Use the first match
    file_id = files[0]["id"]
    mime_type = files[0].get("mimeType", "")

    # Get the file content
    # If it's a Google Doc/Sheet, we'd need to export it. 
    # For regular files, we just download.
    if "application/vnd.google-apps" in mime_type:
        # It's a Google-native format, we must export it to text if possible.
        # Let's try text/plain.
        download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export"
        download_params = {"mimeType": "text/plain"}
    else:
        download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
        download_params = {"alt": "media"}

    content_response = requests.get(download_url, headers=headers, params=download_params)
    if content_response.status_code != 200:
        print(f"Drive API download failed: {content_response.text}")
        hex.set_output("content", "")
        exit(1)

    content = content_response.text

    # 3. Set output
    hex.set_output("content", content)
    print(f"Successfully read {len(content)} characters from Drive file '{filename}'")

except Exception as e:
    print(f"Error reading Drive file: {e}")
    exit(1)

