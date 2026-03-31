import hex
import requests

# --- Gather state and inputs ---
access_token = hex.get_input("access_token")
query = hex.get_input("query")  # optional: filter by name, mime type, etc.

# --- Build the Google Drive API request ---
url = "https://www.googleapis.com/drive/v3/files"

headers = {
    "Authorization": f"Bearer {access_token}",
}

params = {
    "pageSize": 50,  # number of files to fetch
    "fields": "files(id,name,mimeType)",
}

# Optional search query
if query and len(query.strip()) > 0:
    params["q"] = query

# --- Make the API request ---
response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    raise Exception(f"Drive API request failed: {response.text}")

files = response.json().get("files", [])

# --- Format output ---
output_list = [f.get("name") for f in files]

# --- Set output ---
hex.set_output("files", ", ".join(output_list))
