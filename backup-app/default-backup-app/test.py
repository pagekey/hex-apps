import hex

item_source = hex.get_state("item_source")

print(f"Testing auth on {item_source}...")
# Run list on the source item
res = hex.run(item_source, "list")

if res.get("names"):
    print(f"✅ Auth test successful! Files: {res.get('files')}")
else:
    print(f"❌ Auth test failed or no files returned.")
