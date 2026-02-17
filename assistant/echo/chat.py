import hex

# Gather state and inputs.
model_name = hex.get_state("model_name")
prompt = hex.get_input("prompt")

# Print the response
print(f"AI ({model_name}): You said {prompt}")
