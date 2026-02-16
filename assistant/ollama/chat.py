import hex
import requests

# Gather state and inputs.
base_url = hex.get_state("base_url")
model_name = hex.get_state("model_name")
prompt = hex.get_input("prompt")

# Pull the model.
url = f"{base_url}/api/pull"
data = {
    "model": model_name,
}
response = requests.post(url, json=data)

# Generate the response.
url = f"{base_url}/api/generate"
data = {
    "model": model_name,
    "prompt": prompt,
    "stream": False,
}
response = requests.post(url, json=data)
result = response.json()

# Print the response.
print(f"HexBox AI ({model_name}): {result['response']}")
