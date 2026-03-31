import hex

files = hex.run("backup-destination", "list", {"path": "."})

hex.set_output("filenames", files)
