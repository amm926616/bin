#!/usr/bin/env python

import sys
from easy_json_amount import edit_values, read_value, initial_info_setup

initial_info_setup()
amount = int(read_value())

# before adding.
print(f"Before adding: {amount}")

arguments = sys.argv[1:]

if not len(arguments) == 0:
    if arguments[0] == "reset":
        edit_values(0)
        print("Set amount to zero.")
        sys.exit()

for i in arguments:
    amount += int(i) 

edit_values(amount)
print(f"After adding: {amount}")

    

