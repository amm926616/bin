#!/bin/bash

# Check if a .java file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <filename>.java"
  exit 1
fi

# Extract the filename without extension
filename="${1%.*}"

# Compile the Java file
javac "$1"

# Check if compilation was successful
if [ $? -eq 0 ]; then
  # Run the Java program
  java "$filename"
else
  exit 1
fi

