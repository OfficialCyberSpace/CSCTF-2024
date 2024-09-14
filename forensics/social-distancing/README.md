# Social Distancing

- The challenge involves a blocked PowerShell script by Windows Defender.
- The script contained the malware signature of the EICAR test file in a zip (`X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*`).
- The EICAR test file is used for testing antivirus response and is not malicious.
- Windows Defender's Quarantine files are located at `C:\ProgramData\Microsoft\Windows Defender\Quarantine`.
- These files are encrypted using a known method ([details](https://reversingfun.com/posts/how-to-extract-quarantine-files-from-windows-defender/)).
- Using tools like [DeXRAY](https://www.hexacorn.com/blog/2023/10/13/dexray-v2-33/), we can recover the original `.ps1` script from the `ResourceData` file.

```powershell
$hidden = @"
UEsDBAoAAAAAAOCYuCg8z1FoRAAAAEQAAAAJABwAZWljYXIuY29tVVQJAAOUYCw5y1zNZnV4CwAB
BAAAAAAEAAAAAFg1TyFQJUBBUFs0XFBaWDU0KFBeKTdDQyk3fSRFSUNBUi1TVEFOREFSRC1BTlRJ
VklSVVMtVEVTVC1GSUxFISRIK0gqUEsDBAoAAAAAAE8HG1mJ3nc0MQAAADEAAAAEABwAZmxhZ1VU
CQAD9VzNZtVczWZ1eAsAAQQAAAAABAAAAABDU0NURnt5MHVfdW4tcXU0cmFudDFuM2RfbXlfc2Ny
MVB0IV8weDkxYTNlZGZmNn0KUEsBAh4DCgAAAAAA4Ji4KDzPUWhEAAAARAAAAAkAGAAAAAAAAQAA
AKSBAAAAAGVpY2FyLmNvbVVUBQADlGAsOXV4CwABBAAAAAAEAAAAAFBLAQIeAwoAAAAAAE8HG1mJ
3nc0MQAAADEAAAAEABgAAAAAAAEAAACkgYcAAABmbGFnVVQFAAP1XM1mdXgLAAEEAAAAAAQAAAAA
UEsFBgAAAAACAAIAmQAAAPYAAAAAAA==
"@

$decodedBytes = [System.Convert]::FromBase64String($hidden)

$zipFilePath = "malicious.zip"
[System.IO.File]::WriteAllBytes($zipFilePath, $decodedBytes)
```

Here, we see that base64 is decoded and outputted to a zip file called `malicious.zip`.

We can decode the base64 and save it as a zip file and then unzip it to get the flag.
