import hex
import json
import requests

def get_folder_id_by_name(name):
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "q": f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
        "fields": "files(id, name)",
        "pageSize": 1,
    }

    res = requests.get(url, headers=headers, params=params)
    files = res.json().get("files", [])

    if not files:
        return None

    return files[0]["id"]

# 1. Gather context from Hex
access_token = hex.get_state("access_token")
base_path = hex.get_state("base_path")  # Assuming this is a folder ID
filename = hex.get_input("filename")
content = hex.get_input("content")

# 2. Perform the logic
headers = {
    "Authorization": f"Bearer {access_token}",
}

# Search for the file by name (and optionally in a specific folder)
url = "https://www.googleapis.com/drive/v3/files"
if base_path and not base_path.startswith("1"):
    base_path = get_folder_id_by_name(base_path)
q = f"name = '{filename}' and trashed = false"
if base_path:
    q += f" and '{base_path}' in parents"

params = {
    "q": q,
    "fields": "files(id, name, mimeType)",
}

try:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Drive API search failed: {response.text}")
        exit(1)

    files = response.json().get("files", [])
    if files:
        # File exists, update it.
        file_id = files[0]["id"]
        update_url = f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media"
        update_response = requests.patch(update_url, headers=headers, data=content)

        if update_response.status_code != 200:
            print(f"Drive API update failed: {update_response.text}")
            exit(1)

        print(f"Successfully updated Drive file '{filename}' ({file_id})")
    else:
        # File doesn't exist, create it.
        # Step 1: Metadata for the file.
        metadata_url = "https://www.googleapis.com/drive/v3/files"
        metadata = {
            "name": filename,
            "mimeType": "text/plain",
        }
        if base_path:
            metadata["parents"] = [base_path]

        # Use multipart/related for both metadata and content, or just two steps.
        # We'll do two steps for simplicity: create then upload.
        create_response = requests.post(metadata_url, headers=headers, json=metadata)
        if create_response.status_code != 200:
            print(f"Drive API creation failed: {create_response.text}")
            exit(1)

        file_id = create_response.json()["id"]

        # Step 2: Upload the content.
        upload_url = f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media"
        upload_response = requests.patch(upload_url, headers=headers, data=content)

        if upload_response.status_code != 200:
            print(f"Drive API upload failed: {upload_response.text}")
            exit(1)

        print(f"Successfully created Drive file '{filename}' ({file_id})")

    # 3. No specific output for write contract.
    hex.set_output("saved_file_id", file_id)

except Exception as e:
    print(f"Error writing Drive file: {e}")
    exit(1)

