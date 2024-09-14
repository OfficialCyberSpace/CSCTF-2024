# Memory

1. Retrieve the powershell code, one way to do so is with the following command:

```bash
strings -n 10 mem.dmp | grep "flag.jpg" -B 10 -A 30
```

2. Powershell code saves everything in environment variables, so retrieve them using Volatility:

```bash
python volatility3/vol.py -f mem.dmp windows.envars.Envars
```

3. Extract encrypted data, key and IV from envars and decrypt using tool of choice!
