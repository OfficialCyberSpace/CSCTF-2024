#!/usr/local/bin/python3 -u
import os
import os.path
import subprocess
import tempfile

template = """
int _start() {
    %s
}
"""

banned = "{}()#%?"

print("Input your code (1 line)")
code = input("> ")

def fail():
    print("Now that would make things too easy wouldn't it...")
    exit(1)

for c in banned:
    if c in code:
        fail()
        
if "goto" in code:
    fail()

with tempfile.TemporaryDirectory() as td:
    src_path = os.path.join(td, "source.c")
    compiled_path = os.path.join(td, "compiled")
    with open(src_path, "w") as file:
        file.write(template % code)
    
    # bye bye libc and ld, hope you didnt plan on using them
    argv = ["gcc", "-static", "-ffreestanding", "-nostdlib", "-Werror", "-Wall", "-O0", "-o", compiled_path, src_path]
    returncode = subprocess.call(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if returncode != 0:
        print("Oops, there were some compilation errors!")
        exit(1)

    print("Okay hopefully it does something now!")
    subprocess.call([compiled_path])