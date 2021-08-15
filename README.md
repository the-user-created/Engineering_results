# Read this before getting the program for the first time (or when updating the program)

Current version: v2.08

Required Python version: v3.6+

Check the bottom of this README for required packages* (only required for screens below 1080p)

To get this program follow this:

https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

Or just click the green button called "Code" and download the project's zip.

#### Please take note if you have used this before
- Duplicate your results.txt file before using versions v2.xx to be sure that marks do not get corrupted.

---

#### If you are downloading this project for the first time follow the steps below:
1. Rename results_example.json to results.json (or duplicate results_example.json and then rename)
1. Open Command Prompt or Terminal
3. Navigate to the directory where you have downloaded the project file
4. Run the following code next: "python3 results.py"
5. Enter your marks into the respective courses (in decimal or quotient format -- i.e. 0.96 or 24/25 -- 
if you only have percentages, divide the value by 100)
   
You will have to re-run the results.py program if you want to see the updated marks in the "Current Marks for the semester" screen.

#### If you are coming from v1.0x follow the steps below:
1. Open Command Prompt or Terminal
2. Navigate to the directory where you have downloaded the project file
3. Run the following code: "python3 EditMarks.py" (you should only run this program once)
4. Then run the following code: "python3 results.py"
5. Use the program like normal

You will have to re-run the results.py program if you want to see the updated marks in the "Current Marks for the semester" screen.

#### If you are coming from v0.0x follow the steps below:
1. Open Command Prompt or Terminal
2. Navigate to the directory where you have downloaded the project file
3. Run the following code: "python3 make_results_file.py" (you must only run this program once)
4. Then run the following code: "python3 results.py"
5. Use the program like normal

You will have to re-run the results.py program if you want to see the updated marks in the "Current Marks for the semester" screen.

#### *Users on computers with screen resolution below 1080p

1. Open Command Prompt or Terminal
2. Run "pip3 install pyautogui"
3. Use the program like normal

## Keeping your program up-to-date: How-to
Download the latest version of the results.py and replace the current file in your directory with the latest 
versions.

(Make sure that results.json is in the same directory as the new results.py otherwise the program will not run as expected)

Then just run the program.