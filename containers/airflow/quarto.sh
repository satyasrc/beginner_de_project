#!/bin/bash

curl -L -o ~/quarto-1.5.43-linux-arm64.tar.gz https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.43/quarto-1.5.43-linux-arm64.tar.gz
mkdir -p /opt
tar -C /opt -xvzf ~/quarto-1.5.43-linux-arm64.tar.gz

# Rename the extracted folder to a standard name if needed, or just link
# The tarball extracts to 'quarto-1.5.43' usually.
# Let's just link from there.

ln -s /opt/quarto-1.5.43/bin/quarto /usr/local/bin/quarto

# Cleanup
rm ~/quarto-1.5.43-linux-arm64.tar.gz
