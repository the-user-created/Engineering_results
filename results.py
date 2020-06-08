#  Copyright (c) 2020 David Young.
#  All rights reserved
#

'''
THIS PROGRAM ONLY TAKES INTO ACCOUNT YOUR FINAL MARK... NOT WHETHER YOU GET DP
Try not to edit the results.txt file once it has been created... this may cause an untested error.
If you do encounter an error please let me know so that I can fix the problem.

BEWARE: There is very little input error checking in this version of the program
        SOOOO make sure to enter values in the correct format plsssssss :) (as stated in the input prompts)

To use this program:
Before looking through the code run the program and it will ask for all of your results.
Make sure that if you don't have the results for an assessment, you enter '000'... if you don't the program will break.
Once you have entered all your results re-run the program and select the options best suited to your needs.
The program will do what it does and you'll get back:
your final course percentage
the final course percentage you've lost over the semester
and the remaining course percentage to gain

All of this is to date... I can't predict the future... duh ;)

I think that's all, lemme know if there's anything I need to explain about the program and I'll happily do so :)
Good luck
'''

from os.path import exists
import os


class Colors:
    '''
    Used to add colors to text/format the text in certain ways
    '''

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class Fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'


def mam1020f(phy_list):
    result_dict = {'ct1': phy_list[0], 't1': phy_list[1], 't2': phy_list[2], 't3': phy_list[3], 't4': phy_list[4],
                   'final': phy_list[5]}
    # Sorts the dictionary by largest value first
    result_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1], reverse=True)}

    # This loop gathers the marks of each assessment into their respective category
    # and then later calculates the course mark
    # test_c is used to make sure that only the 3 best tests are used for the course mark
    test_c = 0
    # Stored as: [marks you have, marks you have lost]
    ct_avg = [0, 0]
    t_avg = [0, 0]
    final_avg = [0, 0]
    for test, result in result_dict.items():
        if 'ct' in test and 'TBA' not in result:
            ct_avg[0] += eval(result)
            ct_avg[1] += 1 - eval(result)
        elif 't' in test and 'TBA' not in result and test_c < 3:
            t_avg[0] += eval(result)
            t_avg[1] += 1 - eval(result)
            test_c += 1
        elif test == 'final' and 'TBA' not in result:
            final_avg[0] += eval(result)
            final_avg[1] += 1 - eval(result)

    course_mark = 25 * ct_avg[0] + 15 * t_avg[0] + 30 * final_avg[0]
    course_mark_lost = 25 * ct_avg[1] + 15 * t_avg[1] + 30 * final_avg[1]

    print("For MAM1020F:\nYou have: {}%\nYou have lost: {}%\nRemaining: {}%".format(round(course_mark, 2),
                                                                                    round(course_mark_lost, 2), round(
            100 - course_mark - course_mark_lost, 2)))

    return course_mark, course_mark_lost


def phy1012f(phy_list):
    result_dict = {'wps': phy_list[0], 'ct1': phy_list[1], 't2': phy_list[2], 't3': phy_list[3], 't4': phy_list[4],
                   'lab1': phy_list[5], 'lab2': phy_list[6], 'lab3': phy_list[7], 'labt': phy_list[8]}

    # This loop gathers the marks of each assessment into their respective category
    # and then later calculates the course mark
    # Stored as: [marks you have, marks you have lost]
    wps_marks = [0, 0]
    class_test = [0, 0]
    online_tests = [0, 0]
    labs = [0, 0]
    lab_test = [0, 0]
    for test, result in result_dict.items():
        if test == 'ct1':
            class_test[0] += eval(result)
            class_test[1] += 1 - eval(result)

        elif 't' in test and 'l' not in test and 'TBA' not in result:
            online_tests[0] += eval(result)
            online_tests[1] += 1 - eval(result)

        elif 'lab' in test and 't' not in test and 'TBA' not in result:
            labs[0] += eval(result)
            labs[1] += 1 - eval(result)

        elif test == 'labt' and 'TBA' not in result:
            lab_test[0] += eval(result)
            lab_test[1] += 1 - eval(result)

        elif test == 'wps':
            for wps in result_dict[test]:
                if 'TBA' not in wps:
                    wps_marks[0] += eval(wps)
                    wps_marks[1] += 1 - eval(wps)

            # Makes the wps result out of 15 wps's
            wps_marks[0] /= 15
            wps_marks[1] /= 15

    # 30 * class test 1 + 10 * sum of online tests + 10 * wps average
    # + 15 * labs (including one from Q1) * 1/3 + 15 * lab test
    course_mark = 30 * class_test[0] + 10 * online_tests[0] + 10 * wps_marks[0] + 5 * labs[0] + 15 * lab_test[0]
    course_mark_lost = 30 * class_test[1] + 10 * online_tests[1] + 10 * wps_marks[1] + 5 * labs[1] + 15 * lab_test[1]

    print("For PHY1012F:\nYou have: {}%\nYou have lost: {}%\nRemaining: {}%".format(round(course_mark, 2),
                                                                                    round(course_mark_lost, 2), round(
            100 - course_mark - course_mark_lost, 2)))

    return course_mark, course_mark_lost


def csc1015f(csc_list):
    result_dict = {'ass_1': csc_list[0], 'ass_2': csc_list[1], 'ass_3': csc_list[2], 'ass_4': csc_list[3],
                   'ass_5': csc_list[4], 'ass_6': csc_list[5],
                   'ass_7': csc_list[6], 'pt1': csc_list[7], 'pt2': csc_list[8], 'pt3': csc_list[9],
                   'tt1': csc_list[10], 'tt2': csc_list[11], 'tt3': csc_list[12], 'q1': csc_list[13],
                   'q2': csc_list[14], 'q3': csc_list[15], 'q4': csc_list[16], 'q5': csc_list[17], 'q6': csc_list[18],
                   'q7': csc_list[19]}

    # This loop gathers the marks of each assessment into their respective category
    # and then later calculates the course mark
    # Stored as: [marks you have, marks you have lost]
    ass_avg = [0, 0]
    quiz_avg = [0, 0]
    pt_avg = [0, 0]
    theory_avg = [0, 0]
    for test, result in result_dict.items():
        if 'ass' in test and (result == '1' or result == '100/100'):
            ass_avg[0] += 100
        elif 'ass' in test and (result != '1' or result != '100/100') and 'TBA' not in result:
            ass_avg[0] += eval(result)
            ass_avg[1] += 1 - eval(result)
        elif 'pt' in test and (result == '1' or result == '100/100'):
            pt_avg[0] += 100
        elif 'pt' in test and (result != '1' or result != '100/100') and 'TBA' not in result:
            pt_avg[0] += eval(result)
            pt_avg[1] += 1 - eval(result)
        elif 'tt' in test and 'TBA' not in result:
            theory_avg[0] += eval(result)
            theory_avg[1] += 1 - eval(result)
        elif 'q' in test and 'TBA' not in result:
            quiz_avg[0] += eval(result)
            quiz_avg[1] += 1 - eval(result)

    # Assignment Average = 0.9 * Weekly Assignment Average + 0.1 * Quiz Average
    assignment_avg = 0.9 * (ass_avg[0] / 7) + 10 * (quiz_avg[0] / 7)
    assignment_avg_lost = 0.9 * (ass_avg[1] / 7) + 10 * (quiz_avg[1] / 7)

    # Practical Test average  = pt_avg/3
    # Prac_Average = (3/5 * Assignment average + 2/5 * Practical test average)
    prac_avg = 3 / 5 * assignment_avg + 2 / 15 * pt_avg[0]
    prac_avg_lost = 3 / 5 * assignment_avg_lost + 2 / 15 * pt_avg[1]

    # TheoryTest_Average = theory_avg / 3
    # Course_mark = 0.625 * Prac_Average + 0.375 * TheoryTest_Average
    course_mark = 0.625 * prac_avg + 0.125 * theory_avg[0]
    course_mark_lost = 0.625 * prac_avg_lost + 0.125 * theory_avg[1]

    print("For CSC1015F:\nYou have: {}%\nYou have lost: {}%\nRemaining: {}%".format(round(course_mark, 2),
                                                                                    round(course_mark_lost, 2), round(
            100 - course_mark - course_mark_lost, 2)))

    return course_mark, course_mark_lost


def eee1006f(eee_list):
    result_dict = {'ct1': eee_list[0], 'ct2': eee_list[1], 'final': eee_list[2]}

    # This loop gathers the marks of each assessment into their respective category
    # and then later calculates the course mark
    # Stored as: [marks you have, marks you have lost]
    test_1 = [0, 0]
    test_2 = [0, 0]
    final_ass = [0, 0]
    for test, result in result_dict.items():
        if test == 'ct1' and 'TBA' not in result:
            test_1[0] += eval(result)
            test_1[1] += 1 - eval(result)
        elif test == 'ct2' and 'TBA' not in result:
            test_2[0] += eval(result)
            test_2[1] += 1 - eval(result)
        elif 'final' in test and 'TBA' not in result:
            final_ass[0] += eval(result)
            final_ass[1] += 1 - eval(result)

    course_mark = 25 * test_1[0] + 25 * test_2[0] + 50 * final_ass[0]
    course_mark_lost = 25 * test_1[1] + 25 * test_2[1] + 50 * final_ass[1]

    print("For EEE1006F:\nYou have: {}%\nYou have lost: {}%\nRemaining: {}%".format(round(course_mark, 2),
                                                                                    round(course_mark_lost, 2), round(
            100 - course_mark - course_mark_lost, 2)))

    return course_mark, course_mark_lost


def mec1003f(mec_list):
    result_dict = {'schematic': mec_list[0], 'pcb': mec_list[1], 'gerbers': mec_list[2], 'application': mec_list[3]}

    # This loop gathers the marks of each assessment into their respective category
    # and then later calculates the course mark
    # Stored as: [marks you have, marks you have lost]
    schematic = [0, 0]
    pcb = [0, 0]
    gerbers = [0, 0]
    appl = [0, 0]
    for test, result in result_dict.items():
        if test == 'schematic' and 'TBA' not in result:
            schematic[0] += eval(result)
            schematic[1] += 1 - eval(result)
        elif test == 'pcb' and 'TBA' not in result:
            pcb[0] += eval(result)
            pcb[1] += 1 - eval(result)
        elif test == 'gerbers' and 'TBA' not in result:
            gerbers[0] += eval(result)
            gerbers[1] += 1 - eval(result)
        elif 'appl' in test and 'TBA' not in result:
            appl[0] += eval(result)
            appl[1] += 1 - eval(result)

    course_mark = 10 * schematic[0] + 15 * pcb[0] + 20 * gerbers[0] + 55 * appl[0]
    course_mark_lost = 10 * schematic[1] + 15 * pcb[1] + 20 * gerbers[1] + 55 * appl[1]

    print("For MEC1003F:\nYou have: {}%\nYou have lost: {}%\nRemaining: {}%".format(round(course_mark, 2),
                                                                                    round(course_mark_lost, 2), round(
            100 - course_mark - course_mark_lost, 2)))

    return course_mark, course_mark_lost


def get_results(results, course):
    course_results = []
    wps_list = []
    for test, result in results.items():
        if 'TBA' not in test:
            if 'wps' in test:
                wps_list.append(result)

            elif course[:3] in test:
                course_results.append(result)
        else:
            if 'wps' in test:
                wps_list.append(result + 'TBA')

            elif course[:3] in test:
                course_results.append(result + 'TBA')

    if 'phy' in course:
        return [wps_list] + course_results
    else:
        return course_results


def main():
    # Checks if the results.txt file exists in your project directory
    if exists('results.txt'):
        course_input = input("Enter the course code for the course(s) you want to get your course results for: "
                             "(enter 'q' to quit or 'all' for every course)\n")

        if course_input.lower() == 'all':
            courses = ['mam1020f', 'phy1012f', 'csc1015f', 'eee1006f', 'mec1003f']
        else:
            courses = []
            while course_input.lower() != 'q':
                courses.append(course_input.lower())
                course_input = input()

        # All your results will be written in this text file
        file = open('results.txt', 'r+')
        lines = file.readlines()
        file.close()

        # Updates TBA values
        ran_choice = False
        for i in range(0, len(lines)):
            line = lines[i]
            if 'TBA' in line and not ran_choice:
                choice = input("You have empty results (TBA values)... do you want to modify these results? (y/n):\n")
                if choice == 'y':
                    ran_choice = True
                    result = str(input("You may not have completed {} yet. "
                                       "If you have enter your result, if not enter '000':\n"
                                       .format(line[:line.find(':')])))

                    if result != '000':
                        lines[i] = line[:line.find(':') + 1] + 'DONE' + line[line.rfind(':'):line.rfind(':') + 1] \
                                   + result + '\n'
                else:
                    break

            elif 'TBA' in line and ran_choice:
                result = str(input("You may not have completed {} yet. "
                                   "If you have enter your result, if not enter '000':\n"
                                   .format(line[:line.find(':')])))

                if result != '000':
                    lines[i] = line[:line.find(':') + 1] + 'DONE' + line[line.rfind(':'):line.rfind(':') + 1] \
                               + result + '\n'

        # Puts all the results into a dictionary
        results = {}
        # Stores the indexes of each course mark line and their respective course in a dictionary
        cm_indexes = {}
        for line in lines:
            if 'CM' not in line and 'TBA' not in line:
                results.update({line[:line.find(':')]: line[line.rfind(':') + 1:-1]})
            elif 'TBA' in line:
                results.update({line[:line.find(':') + 4]: line[line.rfind(':') + 1:-1]})

            if 'CM' in line:
                cm_indexes.update({line[:3]: lines.index(line)})

        # Calls the respective course functions
        for course in courses:
            # Gets all the marks over the semester from results.txt
            course_marks = get_results(results, course)
            # Gets the final course % and the lost %
            final_mark, final_mark_lost = eval(course + '(' + str(course_marks) + ')')

            # Adds the marks to the course marks section of the respective course in the lines list
            lines[cm_indexes[course[:3]]] = lines[cm_indexes[course[:3]]][:lines[cm_indexes[course[:3]]].rfind(':')+1] \
                                            + str(round(final_mark, 2)) + '/' + str(round(final_mark_lost, 2)) + '\n'
            print()

        # Erases the contents of the file
        os.remove('results.txt')

        modified_file = open('results.txt', 'w+')
        # Writes the lines back to the results.txt file
        modified_file.writelines(lines)
        modified_file.close()

    else:
        file = open('results.txt', 'w+')

        # DO NOT CHANGE THIS --- Initializes the results.txt file
        important_results = [['mam_class_test_1', 'DONE'], ['mam_online_test_1', 'DONE'], ['mam_online_test_2', 'DONE'],
                             ['mam_online_test_3', 'DONE'], ['mam_online_test_4', 'TBA'], ['mam_final_test', 'TBA'],
                             ['mam1020f', 'CM'],

                             ['phy_wps_1', 'DONE'], ['phy_wps_2', 'DONE'], ['phy_wps_3', 'DONE'], ['phy_wps_4', 'DONE'],
                             ['phy_wps_5', 'DONE'], ['phy_wps_8', 'DONE'], ['phy_wps_9', 'DONE'],
                             ['phy_wps_10', 'DONE'], ['phy_wps_11', 'DONE'], ['phy_wps_12', 'DONE'],
                             ['phy_wps_13', 'TBA'], ['phy_wps_14', 'TBA'], ['phy_wps_15', 'TBA'],
                             ['phy_test_1', 'DONE'], ['phy_test_2', 'DONE'], ['phy_test_3', 'TBA'],
                             ['phy_test_4', 'TBA'], ['phy_uct_lab_1', 'DONE'], ['phy_online_lab_1', 'TBA'],
                             ['phy_online_lab_2', 'TBA'], ['phy_online_lab_test', 'TBA'], ['phy1012f', 'CM'],

                             ['eee_class_test_1', 'DONE'], ['eee_class_test_2', 'TBA'], ['eee_final_assignment', 'TBA'],
                             ['eee1006f', 'CM'],

                             ['csc_assignment_1', 'DONE'], ['csc_assignment_2', 'DONE'], ['csc_assignment_3', 'DONE'],
                             ['csc_assignment_4', 'DONE'], ['csc_assignment_5', 'DONE'], ['csc_assignment_6', 'TBA'],
                             ['csc_assignment_7', 'TBA'], ['csc_practical_test_1', 'DONE'],
                             ['csc_practical_test_2', 'DONE'], ['csc_practical_test_3', 'TBA'],
                             ['csc_theory_test_1', 'DONE'], ['csc_theory_test_2', 'TBA'],
                             ['csc_theory_test_3', 'TBA'], ['csc_quiz_1', 'DONE'], ['csc_quiz_2', 'DONE'],
                             ['csc_quiz_3', 'DONE'], ['csc_quiz_4', 'DONE'], ['csc_quiz_5', 'DONE'],
                             ['csc_quiz_6', 'DONE'], ['csc_quiz_7', 'TBA'], ['csc1015f', 'CM'],

                             ['mec_schematic', 'DONE'], ['mec_pcb', 'DONE'], ['mec_gerber', 'TBA'],
                             ['mec_application', 'TBA'], ['mec1003f', 'CM']]

        print("Enter your results in decimal or x/y (e.g. 0.80 or 80/100)")

        for item in important_results:

            if 'wps' not in item[0]:
                if 'pcb' in item[0] and item[1] != 'TBA':
                    result = str(input("What did you get for {}?\n".format(item[0].upper().replace('_', ' '))))

                elif item[1] != 'TBA' and item[1] != 'CM':
                    result = str(input("What did you get for {}?\n"
                                       .format((item[0][:4].upper() + item[0][4:].title()).replace('_', ' '))))

                elif item[1] == 'TBA' and 'pcb' in item[0]:
                    result = str(input("You may not have completed {} yet. "
                                       "If you have enter your result, if not enter '000':\n"
                                       .format((item[0][:4].upper() + item[0][4:].title()).replace('_', ' '))))

                    if result != '000':
                        important_results[important_results.index(item)].insert(1, 'DONE')

                    else:
                        result = '0'

                elif item[1] == 'TBA':
                    result = str(input("You may not have completed {} yet. "
                                       "If you have enter your result, if not enter '000':\n"
                                       .format((item[0][:3].upper() + item[0][3:].title()).replace('_', ' '))))

                    if result != '000':
                        important_results[important_results.index(item)].insert(1, 'DONE')

                    else:
                        result = '0'

            else:
                if item[1] != 'TBA' and item[1] != 'CM':
                    result = str(input("What did you get for {}?\n".format(item[0].upper().replace('_', ' '))))

                elif item[1] == 'TBA':
                    result = str(input("You may not have completed {} yet. "
                                       "If you have enter your result, if not enter '000':\n"
                                       .format(item[0].upper().replace('_', ' '))))

                    if result != '000':
                        important_results[important_results.index(item)].insert(1, 'DONE')
                    else:
                        result = '0'

            if important_results.index(item) != len(important_results) - 1:
                file.write('{}:{}:{}\n'.format(item[0], item[1], result))
            else:
                file.write('{}:{}:{}'.format(item[0], item[1], result))

        file.close()
        print('\n' + Colors.bold + 'RE-RUN THE PROGRAM TO SEE RESULTS')


def fix_csc_08Jun20():
    file = open('results.txt', 'r+')
    lines = file.readlines()
    file.close()
    os.remove('results.txt')
    correct_file = open('results.txt', 'w+')
    for i in range(len(lines)):
        line = lines[i]
        if line[:line.find(':')] == 'csc_quiz_8' or line[:line.find(':')] == 'csc_quiz_9':
            del lines[i]
            break

    for i in range(len(lines)):
        line = lines[i]
        if line[:line.find(':')] == 'csc_quiz_8' or line[:line.find(':')] == 'csc_quiz_9':
            del lines[i]
            break
    correct_file.writelines(lines)
    correct_file.close()
        

if __name__ == '__main__':
    #main()
    fix_csc_08Jun20()

"""
Here's a cat :P
    /\_____/\
   /  o   o  \
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)
"""
