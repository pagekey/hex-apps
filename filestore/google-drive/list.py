import hex
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


# --- Gather state and inputs ---
access_token = hex.get_state("access_token")
base_path = hex.get_state("base_path")
path = hex.get_input("path")  # Treating this as a name filter or folder search

# --- Build the Google Drive API request ---
url = "https://www.googleapis.com/drive/v3/files"

headers = {
    "Authorization": f"Bearer {access_token}",
}

params = {
    "pageSize": 50,
    "fields": "files(id, name, mimeType)",
}

# If path is specified, let's try to filter by name.
# If base_path is provided, we'll filter by parent.
q_parts = ["trashed = false"]

if base_path and not base_path.startswith("1"):
    base_path = get_folder_id_by_name(base_path)

if base_path:
    q_parts.append(f"'{base_path}' in parents")

params["q"] = " and ".join(q_parts)

# --- Make the API request ---
try:
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Drive API request failed ({response.status_code}): {response.text}")
        hex.set_output("names", [])
        exit(1)

    files = response.json().get("files", [])
    names = [f.get("name") for f in files]

    # --- Set output according to contract ---
    hex.set_output("names", names)
    print(f"Found {len(names)} files on Google Drive")

except Exception as e:
    print(f"Error listing Drive files: {e}")
    exit(1)
