#!/bin/bash

echo Hex version:
/opt/pagekey/hexbox/bin/hex version
echo HexBox UI version:
/opt/pagekey/hexbox/bin/hexbox-ui version

echo Update logs:
journalctl -u hexbox-updater -b
