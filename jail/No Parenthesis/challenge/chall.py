#!/usr/local/bin/python3 -u
import os
import os.path
import subprocess
import tempfile

template = """
int main() {
    %s
}
"""

banned = "{}()#%?"

print("Input your code (1 line)")
code = input("> ")

for c in banned:
    if c in code:
        print("Now that would make things too easy wouldn't it...")
        exit(1)

with tempfile.TemporaryDirectory() as td:
    src_path = os.path.join(td, "source.c")
    compiled_path = os.path.join(td, "compiled")
    with open(src_path, "w") as file:
        file.write(template % code)
    
    returncode = subprocess.call(["gcc", "-Werror", "-Wall", "-O0", "-o", compiled_path, src_path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    if returncode != 0:
        print("Oops, there were some compilation errors!")
        exit(1)

    print("Okay hopefully it does something now!")
    subprocess.call([compiled_path])