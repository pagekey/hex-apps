import hex

prompt = hex.get_input("prompt")

value = input(f"{prompt}: ")

hex.set_output("value", value)
