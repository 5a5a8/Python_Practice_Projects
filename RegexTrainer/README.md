# RegexTrainer
A tool I made to help me learn and revise regular expressions.
It reads questions at random from the questions.csv file, which is actually delimited by ' delim ' and has the question to the left of the delimiter and the answer (a regular expression) to the right of the delimiter.
Currently there are not many questions and there is not much data to search.

The data to be searched is stored in data.txt.
It contains both valid and invalid data (e.g. Invalid IPv4 addresses).
Though you can make the questions whatever you want, the idea is to not return invalid data.

Once it has chosen a question, it will print the expected result and prompt the user for a regular expression.
If the regex entered by the user returns the same lines as the one in the answer, it considers the user input to be correct i.e. the user does not have to enter the same regex as the answer, just one that matches the same lines.

I learnt about regular expressions the day before I wrote this code, so the answers provided will not be perfect.

Written 2020-10-31.
