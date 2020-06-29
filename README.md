# Read this before running the program for the first time (or when updating the program)

Current version: v0.06

To get this program follow this:

https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

Or just click download zip.

Please let me know if you encounter an error in the program :)

Ignore the section below if downloading for the first time.

## If your marks on an previous assessment change:
Open the results.txt file, make sure you open it in a text editor, not a word processor.

Look in the file for the name of the assessment which has changed.

Once you have found the assessment, change the value after the last colon to match the new marks.

WARNING: Make sure the line you've just modified has a colon after the assessment name and after 'DONE' 
(sometimes 'TBA') e.g. phy_test_3:DONE:0/25

## Keeping your program up-to-date: How-to
You have two methods to choose from.

#### The slightly hands-on method:
Download the latest version of the results.py and replace the current results.py in your directory with the latest 
version. 

(Make sure that results.txt is in the same directory as the new results.py otherwise it'll break)

Then comment the call for main() and uncomment fix(some_list, another_list, something_else) at the end of the program.

Run the program once.

Then comment fix() and uncomment main().

#### The completely hands-on method:
View the changelog corresponding to your current version of the program and adjust the program accordingly.