# HamRadioLog
This project was written one afternoon in Spring when it was raining out of a low sky.
It provides a contact logging functionality for amateur radio operators.

You will need pandas installed to view your logs from within the program, however the log is a pipe separated value file so you should also be able to view it with any spreadsheet software.

Run the program with 'python HamRadioLog.py'

## Profiles
Profiles allow you to autofill most of your data during an operating session.
You can start a profile with your data, such as your callsign, frequencies, and modes.
When you make a contact using this profile, you will only have to enter your contacts callsign, name, and any notes about the contact.
Profiles can be edited from the main screen. Adding, editing, and deleting profiles should be self-explanatory.

## Log Previous QSOs
If you made some contacts outside of an operating session, you can log them manually here.
You will need to enter the date manually, formatted as DD MMHHz Mon YY.
You will also need to manually enter any other details about the contact.

## Profiled Operating Session
Profiled sessions work best when you know you will be working a specific frequency and mode for a period of time.
For example if you know you're about to spend an hour on 147.500 FM Simplex, you can choose a profile with that set up.
When someone contacts you during a session, you just push s, and all of that data is filled automatically in the log.
The time of the contact will be logged automatically, you will only have to enter any data not covered by the profile (callsign, name, notes).

## Non-Profiled Operating Session
This is similar to a profiled operating session, but you will have to enter all information except for the time manually.
You would use this mode if you were planning to monitor a range of frequencies and modes in a short amount of time.

## View the Log
The log is viewed as a Pandas data frame. There isn't really anything special here.

## Sort the Log
If you have entries in your log that are not sorted by date (maybe you manually entered some contacts from a few days prior), then this will sort by the date time group. The most recent entries will go to the bottom.

## Misc
This was pretty much hacked together in an afternoon for a learning project.
As I wrote it I noticed better ways of doing things to what I had done previously, but didn't necessarily go back and make the changes as I'd already had the learning experience.
I might make the changes if this gets any interest, but I don't expect it to.
That said, feedback and bug reports are welcome.
