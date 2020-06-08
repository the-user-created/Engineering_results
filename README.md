To get this program follow this:

https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

Or just click download zip :)

## CSC1015F UPDATE (Jun-08-2020)

Either re-download the program and it'll fix everything

Then delete the function fix_csc_08Jun20()

And delete the function call at the end of the program and un-comment main()

Oh, and also, just replace the current results.py program in your directory with the new one :)

^^^this only applies to the previous version of the program, ignore if downloading for the first time.

### OR

Only applies to the previous version, if only downloading the program after 7th Jun, ignore this :)

Do the following:

#### On line 156:

Change:

... 'q7': csc_list[19], 'q8': csc_list[20], 'q9': csc_list[21]}

To:

... 'q7': csc_list[19]}

#### On line 184:

Change:

assignment_avg = 0.9 * (ass_avg[0] / 7) + 10 * (quiz_avg[0] / 9)

To:

assignment_avg = 0.9 * (ass_avg[0] / 7) + 10 * (quiz_avg[0] / 7)

#### On line 185:

Change:

assignment_avg_lost = 0.9 * (ass_avg[1] / 7) + 10 * (quiz_avg[1] / 9)

To:

assignment_avg_lost = 0.9 * (ass_avg[1] / 7) + 10 * (quiz_avg[1] / 7)

#### On line 396 and 397:

Change:

... ['csc_quiz_6', 'DONE'], ['csc_quiz_7', 'TBA'], ['csc_quiz_8', 'TBA'],
                             ['csc_quiz_9', 'TBA'], ['csc1015f', 'CM'], ...

To:

... ['csc_quiz_6', 'DONE'], ['csc_quiz_7', 'TBA'], ['csc1015f', 'CM'], ...

#### In results.txt:

Remove the following lines

csc_quiz_8:TBA:0

csc_quiz_9:TBA:0
