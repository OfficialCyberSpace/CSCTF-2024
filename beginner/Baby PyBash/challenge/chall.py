#!/usr/local/bin/python3 -u
import re
import subprocess


def restrict_input(command):
    pattern = re.compile(r'[a-zA-Z*^\,,;\\!@/#?%`"\'&()-+]|[^\x00-\x7F]')
    if pattern.search(command):
        raise ValueError("that's not nice!")
    return command


def execute_command(command):
    safe = restrict_input(command)
    result = subprocess.run(safe, stdout=True, shell=True)
    return result.stdout


print("Welcome to Baby PyBash!\n")
cmd = input("Enter a bash command: ")
output = execute_command(cmd)
print(output)
