# DoNotRun
Do not run this code.

This is a simple virus written in Python, for Linux systems.
I wrote it on 2020-Nov-08, to learn about malware.

It searches for other `.py` files and then opens them to check for a signature.
If it finds that signature, the file is already infected, so we skip it.
If it doesn't, it adds the signature and infects the file.

Finally, it checks for some condition specified in the settings.
If that condition is met, it runs the `bomb` function. 
Currently, this function does nothing harmful, but it could be changed.

## Run
To see the code in action (not recommended), you need to modify `virus.py`.

- comment out `sys.exit()` (this is in case the program is run accidentally)
- set `mode = 'unsafe'`

When you run the virus, it will check its privelege level.
If it is run as root, it will start scanning at the root directory.
Otherwise it will scan the user's home directory.

If you run it with `mode = 'safe'` it will scan the current working directory.
