#!/bin/bash

# Check if xclip is installed
if command -v xclip &> /dev/null; then
    echo -n "hellothere" | xclip -selection clipboard
else
    echo "xclip is not installed. Please install it using your package manager."
fi
