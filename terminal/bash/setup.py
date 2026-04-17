import hex

user_input_item = hex.get_state("user_input_item") or "cli-user-input"
hex.set_state("user_input_item", user_input_item)

if not hex.get_item(user_input_item):
    hex.create_item(user_input_item, "cli-user-input", emoji="⌨️")

print(f"Terminal setup complete with user input provider: {user_input_item}")
