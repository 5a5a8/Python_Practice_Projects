# CryptoJournal

This software searches for `.md` files in a directory and archives them.
It will then encrypt the archive with AES 256.
The encrypted file is then sent to dropbox.

All of the local files are removed.
This software can also do the above in reverse, to get your files back.

This will eventually be moved to its own repository, but there is more work to do before then.
This is not really a public release.


## Installation
`pip install -r requirements.txt`

This software is also designed to be run from the system path.

`sudo cp cryptojournal.py /usr/local/bin/cjournal`

`sudo chmod +x /usr/local/bin/cjournal`


## Dropbox Setup
1. Register for [Dropbox](https://dropbox.com)
2. Register a new app in the [App Console](https://www.dropbox.com/developers/apps/create)
3. Choose scoped access
4. App Folder
5. Name it CryptoJournal
6. Go to the app console
7. In the permissions tab, enable `files.content.write` and `files.content.read`
8. Go to the settings tab, and generate a new access token with no expiry
9. Make a note of the access token, you will need it later


## Usage
Before we do anything, we need to initialise a directory.
This is the directory where we will store our journal files.
This software will only look for markdown (.md) files, because that's how the author likes to keep his journal.

Initialise a directory with `cjournal --init`. 
You will be prompted for a password, the journal name, and your Dropbox token that you should have created earlier.
Two new files will be created.
The `.initfile` contains the hash and salt of your password.
The `.dbx` file contains the dropbox token and name of the journal.

Now you can start writing your journal.
Once you have some `.md` files, run `cjournal --push` to compress, encrypt, and send to Dropbox.

The `.md` files will be removed from your local system.
The idea is to run `cjournal --pull` to retrieve and decrypt them.

There are also the arguments `--localpush` and `--localpull` which do the same as the above, but don't send to dropbox.

## Misc.
This version written and released on 2020-Nov-14.
