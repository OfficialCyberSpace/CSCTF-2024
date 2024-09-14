# ZipZone

This is a beginner web challenge, it is a simple file server that serves files after unzipping them. The vulnerability is pretty simple, in [app.py](challenge/app/app.py), we can see that the server executes `unzip` on the file that is requested by the user.

```py
subprocess.call(["unzip", filename, "-d", f"{upload_dir}files/{upload_uuid}"])
```

This vulnerability can be exploited through a symlink attack. By creating a symlink to `/tmp/flag.txt` and then requesting the symlinked file, an attacker can gain unauthorized access to the flag. To demonstrate this, we can create a zip archive that contains a symlink pointing to `/tmp/flag.txt` and then extract or request the file through the symlink to retrieve the flag.

```bash
touch /tmp/flag.txt
ln -s /tmp/flag.txt exp
zip --symlink exp.zip exp
```

Then, simply upload the `exp.zip` file, navigate to the unique UUID that is generated and append `/exp` to get the flag.
