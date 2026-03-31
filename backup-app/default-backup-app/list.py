import hex

source = hex.get_input("source")

files = hex.run("filestore", "list", {"path": source})["names"]

hex.set_output("filenames", files)
