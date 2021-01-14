# PassMan

This is password manager written in Python.
It was written for learning purposes, if you are going to use it with real data, do so at your own risk.
I certainly won't be using it.

## Authentication
We use bcrypt for authentication and key derivation.
We then use this derived key for encryption of the data using Fernet, or AES-128.

## Entry Types
This currently supports two types of entries: Login details, and credit card details.
You can create them, read them, update them, and delete them.

## Check Breaches
There is an option to check all of your password entries against the haveibeenpwned API to see if any are breached.
We send the first 5 characters of the SHA-1 hash, and for any matches, it returns the suffix of the hash.
Their documentation indicates we generally can expect about 500 suffixes in return.
We prepend the first 5 characters of our hash to each one and check it against the full hash.
If we get a match, the password was breached.
It will also tell you how many times said password was breached.
