import hex

item_auth = hex.get_state("item_auth") or "google-auth"
access_token = hex.get_state("access_token")

print(f"Testing auth on {item_auth}...")
# Run test on the auth item
res = hex.run(item_auth, "test", {"access_token": access_token, "path": ".", "query": ""})

if res.get("files"):
    print(f"✅ Auth test successful! Files: {res.get('files')}")
else:
    print(f"❌ Auth test failed or no files returned.")

