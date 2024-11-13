#!/usr/bin/env python

from random import randint
from time import sleep

print("Will I get passed the eps exam with my mark sharp 80?")

for i in range(3):
    print(i + 1)
    sleep(1)

print("For only testing purpose.")

if (randint(0, 1)):
    print("Don't worry, you will get selected")
else:
    print("You should get prepared and hope for the best")
