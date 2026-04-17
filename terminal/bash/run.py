import hex
import subprocess

command = hex.get_input("command")
user_input_item = hex.get_state("user_input_item")

if not command:
    if user_input_item:
        print("No command provided in inputs. Requesting from user-input...")
        res = hex.run(user_input_item, "get_string", {"prompt": "Enter terminal command"})
        command = res.get("value")
    
if not command:
    print("Error: No command provided.")
    exit(1)

print(f"Running command: {command}")
try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    hex.set_output("output", result.stdout + result.stderr)
    hex.set_output("exit_code", result.returncode)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
except Exception as e:
    print(f"Error executing command: {e}")
    hex.set_output("output", str(e))
    hex.set_output("exit_code", 1)
