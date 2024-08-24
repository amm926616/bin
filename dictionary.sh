#!/bin/bash

# Define the alias you want to add
alias_name="personal-dictionary"
alias_command="python3 /home/adam178/MyGitRepos/sqlite-personal-dictionary/main.py"

# Add the alias to the user's .bashrc file
echo "alias $alias_name='$alias_command'" >> ~/.bashrc

# Optionally, source the .bashrc file to apply the changes immediately
source ~/.bashrc

# Notify the user
echo "Alias '$alias_name' has been added. You can now use it in your terminal."
