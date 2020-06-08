To get this program follow this:

https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

Or just click download zip :)

## CSC1015F UPDATE (Jun-08-2020)

Either re-download the program and it'll fix everything

Then delete the function fix_csc_08Jun20()

And delete the function call at the end of the program and un-comment main()

### OR

Do the following:

### On line 184:

Change:

assignment_avg = 0.9 * (ass_avg[0] / 7) + 10 * (quiz_avg[0] / 9)

To:

assignment_avg = 0.9 * (ass_avg[0] / 7) + 10 * (quiz_avg[0] / 7)

### On line 185:

Change:

assignment_avg_lost = 0.9 * (ass_avg[1] / 7) + 10 * (quiz_avg[1] / 9)

To:

assignment_avg_lost = 0.9 * (ass_avg[1] / 7) + 10 * (quiz_avg[1] / 7)

### On line 396 and 397:

Change:

... ['csc_quiz_6', 'DONE'], ['csc_quiz_7', 'TBA'], ['csc_quiz_8', 'TBA'],
                             ['csc_quiz_9', 'TBA'], ['csc1015f', 'CM'], ...

To:

... ['csc_quiz_6', 'DONE'], ['csc_quiz_7', 'TBA'], ['csc1015f', 'CM'], ...

### In results.txt:

Remove the following lines

csc_quiz_8:TBA:0

csc_quiz_9:TBA:0
