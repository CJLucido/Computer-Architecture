#!/usr/bin/env python3

"""Main."""

import sys
# import re
from cpu import *

file = open(sys.argv[1], "r")
file_content = file.read()
instruction_list = []
# print(file_content.splitlines())
for line in file_content.splitlines():
    instruction = line.split(" ")[0]
    # instruction = re.split(" | \n| #", line)[0]
    # print(instruction)
    if len(instruction) == 8:
        instruction_list.append(instruction)
    # instruction_list.append("0b" + instruction)

file.close()


# print(instruction_list)
cpu = CPU()

cpu.load(instruction_list)
cpu.run()