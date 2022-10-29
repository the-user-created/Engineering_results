#  Copyright (c) 2021 David Young.
#  All rights reserved
#

# v2.21

from datetime import date
import json
import os
from tkinter import *
from tkinter import messagebox

errors = []

try:
    import pyautogui

    width, height = pyautogui.size()
except AttributeError or ModuleNotFoundError as e:
    if e == ModuleNotFoundError:
        errors.append("pyautogui")

    height = 1080
    pass

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    errors.append("matplotlib")
    pass

try:
    import numpy as np
except ModuleNotFoundError as e:
    errors.append("numpy")
    pass

data = {}
years = {1: "first_year", 2: "second_year", 3: "third_year", 4: "fourth_year"}
courses_by_year = {"first_year": ["mam1020f", "phy1012f", "eee1006f", "csc1015f", "mec1003f",
                                  "mam1021s", "phy1013s", "csc1016s", "eee1007s", "axl1200s"],
                   "second_year": ["eee2045f", "eee2046f", "eee2048f", "mam2083f", "mec1009f",
                                   "eee2044s", "eee2047s", "mam2084s", "con2026s", "phy2010s"],
                   "third_year": ["csc2001f", "eee3088f", "eee3089f", "eee3090f", "eee3092f",
                                  "csc2002s", "eee3093s", "eee3094s", "eee3096s", "eee3097s"]
                   }
courses_by_semester = {"y1s1": ["mam1020f", "phy1012f", "eee1006f", "csc1015f", "mec1003f"],
                       "y1s2": ["mam1021s", "phy1013s", "csc1016s", "eee1007s", "axl1200s"],
                       "y2s1": ["eee2045f", "eee2046f", "eee2048f", "mam2083f", "mec1009f"],
                       "y2s2": ["eee2044s", "eee2047s", "mam2084s", "con2026s", "phy2010s"],
                       "y3s1": ["csc2001f", "eee3088f", "eee3089f", "eee3090f", "eee3092f"],
                       "y3s2": ["csc2002s", "eee3093s", "eee3094s", "eee3096s", "eee3097s"]
                       }  # {"year-year_#-semester-semester_#": [course 1, course 2, ...]}


def calculate_marks(course, course_marks):
    course_grade_values = {}
    have, lost, course_grade, weighting = 0, 0, 0, 0

    # TODO: - FINISH ADDING THE COURSE GRADE CALCULATIONS TO THE COURSES
    """
    course_grade_values = {"": [0, 0, 0], "": [0, 0, 0], "": [0, 0, 0], "": [0, 0, 0]}
    
    course_grade_values[""][0] += 1
    course_grade_values[""][1] += eval(v)
    """

    # First Year, first semester
    if course == "mam1020f":
        course_grade_values = {"class": [0, 0, 25], "final": [0, 0, 30], "test": [0, 0, 45]}
        # Case 1:
        test_count, final_test_have, final_test_lost, test_have, test_lost, class_tests_have, class_tests_lost = 0, 0, 0, 0, 0, 0, 0
        tests = []

        for (k, v) in course_marks:
            if v == "":
                continue

            if "class" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
                course_grade_values["class"][0] += 1
                course_grade_values["class"][1] += eval(v)
            elif "final" in k:
                final_test_have += eval(v)
                final_test_lost += 1 - eval(v)
                course_grade_values["final"][0] += 1
                course_grade_values["final"][1] += eval(v)
            elif "test" in k:
                tests.append([k, v])
                test_count += 1
                if test_count == 4:
                    tests.sort(key=lambda l: l[1], reverse=True)
                    for test in tests[:3]:
                        test_have += eval(test[1])
                        test_lost += 1 - eval(test[1])
                        course_grade_values["test"][0] += 1
                        course_grade_values["test"][1] += eval(test[1])

        have = 25 * class_tests_have + 15 * test_have + 30 * final_test_have
        lost = 25 * class_tests_lost + 15 * test_lost + 30 * final_test_lost

    elif course == "csc1015f":
        quizzes_have, quizzes_lost, practical_have, practical_lost, theory_have, theory_lost, assignment_have, assignment_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "quiz" in k:
                quizzes_have += eval(v)
                quizzes_lost += 1 - eval(v)
            elif "practical_test" in k:
                practical_have += eval(v)
                practical_lost += 1 - eval(v)
            elif "theory" in k:
                theory_have += eval(v)
                theory_lost += 1 - eval(v)
            elif "assignment" in k:
                assignment_have += eval(v)
                assignment_lost += 1 - eval(v)

        practical_avg_have = 0.6 * (0.1 * (quizzes_have / 7) + 0.9 * (assignment_have / 7)) + 0.4 * (practical_have / 2)
        practical_avg_lost = 0.6 * (0.1 * (quizzes_lost / 7) + 0.9 * (assignment_lost / 7)) + 0.4 * (practical_lost / 2)
        have = 100 * (0.625 * practical_avg_have + 0.375 * (theory_have / 3))
        lost = 100 * (0.625 * practical_avg_lost + 0.375 * (theory_lost / 3))

    elif course == "eee1006f":
        for (k, v) in course_marks:
            if v == "":
                continue

            if "test" in k:
                have += 25 * eval(v)
                lost += 25 * (1 - eval(v))
            else:
                have += 50 * eval(v)
                lost += 50 * (1 - eval(v))

    elif course == "phy1012f":
        first_test_have, first_test_lost, lab_test_have, lab_test_lost, class_tests_have, class_tests_lost, \
        wps_have, wps_lost, labs_have, labs_lost = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "test_1" in k:
                first_test_have += eval(v)
                first_test_lost += 1 - eval(v)
            elif "lab_test" in k:
                lab_test_have += eval(v)
                lab_test_lost += 1 - eval(v)
            elif "test" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "wps" in k:
                wps_have += eval(v)
                wps_lost += 1 - eval(v)
            elif "lab" in k:
                labs_have += eval(v)
                labs_lost += 1 - eval(v)

        have = 30 * first_test_have + 10 * class_tests_have + 10 * (wps_have / 14) + 15 * (
                labs_have / 4) + 15 * lab_test_have
        lost = 30 * first_test_lost + 10 * class_tests_lost + 10 * (wps_lost / 14) + 15 * (
                labs_lost / 4) + 15 * lab_test_lost

    elif course == "mec1003f":
        # TODO - Confirm that this formula is correct

        for (k, v) in course_marks:
            if v == "":
                continue

            if "application" in k:
                have += eval(v) * 55
                lost += (1 - eval(v)) * 55
            elif "gerber" in k:
                have += eval(v) * 20
                lost += (1 - eval(v)) * 20
            elif "pcb" in k:
                have += eval(v) * 15
                lost += (1 - eval(v)) * 15
            elif "schematic" in k:
                have += eval(v) * 10
                lost += (1 - eval(v)) * 10

    # First Year, second semester
    elif course == "csc1016s":
        # TODO - Using correct formula as shown in the Notes to Students... however incorrect output

        assignment_have, assignment_lost, quizzes_have, quizzes_lost, practical_test_have, practical_test_lost, theory_have, theory_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "assignment" in k:
                assignment_have += eval(v)
                assignment_lost += 1 - eval(v)
            elif "quiz" in k:
                quizzes_have += eval(v)
                quizzes_lost += 1 - eval(v)
            elif "practical_test" in k:
                practical_test_have += eval(v)
                practical_test_lost += 1 - eval(v)
            elif "theory" in k:
                theory_have += eval(v)
                theory_lost += 1 - eval(v)

        practical_average_have = 0.9 * (assignment_have / 6) + 0.1 * (quizzes_have / 7)
        practical_average_lost = 0.9 * (assignment_lost / 6) + 0.1 * (quizzes_lost / 7)
        have = 36 * practical_average_have + 24 * (practical_test_have / 2) + 40 * (theory_have / 3)
        lost = 36 * practical_average_lost + 24 * (practical_test_lost / 2) + 40 * (theory_lost / 3)

    elif course == "mam1021s":
        quizzes_have = 0
        quizzes_lost = 0
        quizzes = {}
        for (k, v) in course_marks:
            if v == "":
                continue

            if v != "":
                if "quiz" in k:
                    quizzes.update({k: v})
                elif "final" in k:
                    have += eval(v) * 25
                    lost += (1 - eval(v)) * 25
                elif "test" in k:
                    have += eval(v) * 20
                    lost += (1 - eval(v)) * 20

        quizzes = {k: v for k, v in sorted(quizzes.items(), key=lambda item: eval(item[1]), reverse=True)}

        j = 0
        for i in quizzes.values():
            if j < 8:
                quizzes_have += eval(i)
                quizzes_lost += 1 - eval(i)
                j += 1
            else:
                continue

        have += (quizzes_have * 15) / 8
        lost += (quizzes_lost * 15) / 8

    elif course == "phy1013s":
        class_tests_have, class_tests_lost, wps_have, wps_lost, lab_test_have, lab_test_lost, labs_have, labs_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "test_" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "wps" in k:
                wps_have += eval(v)
                wps_lost += 1 - eval(v)
            elif "lab_test" in k:
                lab_test_have = eval(v) * 7.5
                lab_test_lost = (1 - eval(v)) * 7.5
            elif "lab" in k:
                labs_have += eval(v)
                labs_lost += 1 - eval(v)

        wps_have = 10 * (wps_have / 12)
        wps_lost = 10 * (wps_lost / 12)

        have += wps_have + lab_test_have + 7.5 * (labs_have / 4) + 75 * (class_tests_have / 4)
        lost += wps_lost + lab_test_lost + 7.5 * (labs_lost / 4) + 75 * (class_tests_lost / 4)

    elif course == "eee1007s":
        class_tests_have, class_tests_lost, assignment_have, assignment_lost = 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "test_" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "assignment" in k:
                assignment_have = eval(v)
                assignment_lost = 1 - eval(v)

        have = class_tests_have * 35 + assignment_have * 30
        lost = class_tests_lost * 35 + assignment_lost * 30

    elif course == "axl1200s":
        reflection_have, reflection_lost, research_have, research_lost = 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "reflection" in k:
                reflection_have += eval(v)
                reflection_lost += 1 - eval(v)
            elif "research_project" in k:
                research_have += eval(v)
                research_lost += (1 - eval(v))

        have += 70 * (reflection_have / 7) + 30 * research_have
        lost += 70 * (reflection_lost / 7) + 30 * research_lost

    # Second Year, first semester
    elif course == "eee2045f":
        class_tests_have, class_tests_lost, exam_have, exam_lost, lab_have, lab_lost, \
        assignment_have, assignment_lost, tut_test_have, tut_test_lost = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "tutorial" in k:
                tut_test_have += eval(v)
                tut_test_lost += 1 - eval(v)
            elif "class" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "pre" in k:
                assignment_have += eval(v)
                assignment_lost += 1 - eval(v)
            elif "lab" in k:
                lab_have += eval(v)
                lab_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        have = 60 * exam_have + 10 * class_tests_have + (10 / 3) * assignment_have + (
                5 / 3) * lab_have + 1.25 * tut_test_have
        lost = 60 * exam_lost + 10 * class_tests_lost + (10 / 3) * assignment_lost + (
                5 / 3) * lab_lost + 1.25 * tut_test_lost

    elif course == "eee2046f":
        class_tests_have, class_tests_lost, exam_have, exam_lost, practical_have, practical_lost = 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "practical" in k:
                practical_have += eval(v)
                practical_lost += 1 - eval(v)
            elif "test" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        have = 60 * exam_have + 12.5 * class_tests_have + 3.75 * practical_have
        lost = 60 * exam_lost + 12.5 * class_tests_lost + 3.75 * practical_lost

    elif course == "eee2048f":
        practical_have, practical_lost, app_have, app_lost, academic_have, academic_lost, mcq_have, mcq_lost, \
        report_have, report_lost, capstone_proposal_have, capstone_proposal_lost, capstone_report_have, \
        capstone_report_lost = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "capstone_report" in k:
                capstone_report_have += eval(v)
                capstone_report_lost += 1 - eval(v)
            elif "capstone" in k:
                capstone_proposal_have += eval(v)
                capstone_proposal_lost += 1 - eval(v)
            elif "practical" in k:
                practical_have += eval(v)
                practical_lost += 1 - eval(v)
            elif "application" in k:
                app_have += eval(v)
                app_lost += 1 - eval(v)
            elif "academic" in k:
                academic_have += eval(v)
                academic_lost += 1 - eval(v)
            elif "multiple" in k:
                mcq_have += eval(v)
                mcq_lost += 1 - eval(v)
            elif "report" in k:
                report_have += eval(v)
                report_lost += 1 - eval(v)

        have = 0.25 * (25 * practical_have + 100 * app_have + 30 * academic_have + 20 * mcq_have + 30 * report_have) + \
               0.25 * (10 * capstone_proposal_have + 110 * capstone_report_have)
        lost = 0.25 * (25 * practical_lost + 100 * app_lost + 30 * academic_lost + 20 * mcq_lost + 30 * report_lost) + \
               0.25 * (10 * capstone_proposal_lost + 110 * capstone_report_lost)

    elif course == "mam2083f":
        quizzes_have, quizzes_lost, tut_total_have, tut_total_lost, ct1_have, ct1_lost, ct2_have, ct2_lost, \
        exam_have, exam_lost = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        using_tut_total = False

        for (k, v) in course_marks:
            if v == "":
                continue

            if "quiz" in k:
                quizzes_have += eval(v)
                quizzes_lost += 1 - eval(v)
            elif "tutorial_total" in k:
                if v != "":
                    using_tut_total = True
                tut_total_have += eval(v)
                tut_total_lost += 1 - eval(v)
            elif k == "test_1":
                ct1_have += eval(v)
                ct1_lost += 1 - eval(v)
            elif k == "test_2":
                ct2_have += eval(v)
                ct2_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        class_record_have = (2 * ct2_have + ct1_have + (tut_total_have if using_tut_total else (quizzes_have / 10))) / 4
        class_record_lost = (2 * ct2_lost + ct1_lost + (tut_total_lost if using_tut_total else (quizzes_lost / 10))) / 4

        have_1 = (3 * exam_have + 2 * class_record_have) / 5
        have_2 = (4 * exam_have + class_record_have) / 5

        if have_1 >= have_2:
            have = 100 * have_1
            lost = 100 * (3 * exam_lost + 2 * class_record_lost) / 5
        else:
            have = 100 * have_2
            lost = 100 * (4 * exam_lost + class_record_lost) / 5

    elif course == "mec1009f":
        tutorials = {}
        tests = {}

        class_tests_have, class_tests_lost, tut_test_have, tut_test_lost = 0, 0, 0, 0
        adjusted_marks = {}
        exam_k, exam_v = course_marks[-1]
        exam_have = eval(exam_v) if exam_v != "" else 0
        exam_lost = 1 - eval(exam_v) if exam_v != "" else 0

        for (k, v) in course_marks:
            temp_v = v
            if exam_have != 0:
                temp_v = v if exam_have < eval(v) else str(exam_have)

            if "tutorial" in k:
                tutorials.update({k: temp_v})
            elif "test" in k:
                tests.update({k: temp_v})

            adjusted_marks.update({k: temp_v})

        tutorials = {k: v for k, v in sorted(tutorials.items(), key=lambda item: eval(item[1]), reverse=True)}
        tests = {k: v for k, v in sorted(tests.items(), key=lambda item: eval(item[1]), reverse=True)}

        i = 0
        for k, v in tutorials.items():
            tut_test_have += eval(v)
            tut_test_lost += 1 - eval(v)
            if i == 2:
                i = 0
                break
            i += 1

        for k, v in tests.items():
            class_tests_have += eval(v)
            class_tests_lost += 1 - eval(v)
            if i == 1:
                break
            i += 1

        have = 60 * exam_have + 40 * (0.25 * (tut_test_have / 3) + 0.75 * (class_tests_have / 2))
        lost = 60 * exam_lost + 40 * (0.25 * (tut_test_lost / 3) + 0.75 * (class_tests_lost / 2))

    # Second Year, second semester
    elif course == "con2026s":
        main_assign_have, main_assign_lost, general_have, general_lost, ct_have, ct_lost, exam_have, exam_lost = 0, 0, 0, 0, 0, 0, 0, 0

        general_assignments = ["1.A1", "1.A2", "3.A1", "4.A2", "5.A1", "6.A1"]
        main_assignment = ["2.A1", "3.A2", "4.A1", "7.A1", "8.A1", "10.A1"]

        for k, v in course_marks:
            if v == "":
                continue

            if k[:k.find("_")] in general_assignments:
                general_have += eval(v)
                general_lost += 1 - eval(v)
            elif k[:k.find("_")] in main_assignment or "main" in k:
                main_assign_have += eval(v)
                main_assign_lost += 1 - eval(v)
            elif "test" in k:
                ct_have += eval(v)
                ct_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        have = 30 * exam_have + 20 * ct_have + 30 * main_assign_have / 7 + 20 * general_have / 6
        lost = 30 * exam_lost + 20 * ct_lost + 30 * main_assign_lost / 7 + 20 * general_lost / 6

    elif course == "eee2044s":
        lab_have, lab_lost, project_have, project_lost, class_tests_have, class_tests_lost, \
        exam_have, exam_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "lab" in k:
                lab_have += eval(v)
                lab_lost += 1 - eval(v)
            elif "project" in k:
                project_have += eval(v)
                project_lost += 1 - eval(v)
            elif "test" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        have = 60 * exam_have + 15 * class_tests_have + 4 * project_have + lab_have
        lost = 60 * exam_lost + 15 * class_tests_lost + 4 * project_lost + lab_lost

    elif course == "eee2047s":
        ps_have, ps_lost, lab_have, lab_lost, class_test_have, class_test_lost, \
        exam_have, exam_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "problem" in k:
                ps_have += eval(v)
                ps_lost += 1 - eval(v)
            elif "lab" in k:
                lab_have += eval(v)
                lab_lost += 1 - eval(v)
            elif "test" in k:
                class_test_have += eval(v)
                class_test_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        have = 60 * exam_have + 20 * class_test_have + 10 * (lab_have / 3) + 10 * (ps_have / 3)
        lost = 60 * exam_lost + 20 * class_test_lost + 10 * (lab_lost / 3) + 10 * (ps_lost / 3)

    elif course == "mam2084s":
        webwork_have, webwork_lost, class_test_have, class_test_lost, exam_have, exam_lost = 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "webwork" in k:
                webwork_have += eval(v)
                webwork_lost += 1 - eval(v)
            elif "test" in k:
                class_test_have += eval(v)
                class_test_lost += 1 - eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)

        class_record_have = 20 * (webwork_have / 5) + 40 * class_test_have
        class_record_lost = 20 * (webwork_lost / 5) + 40 * class_test_lost

        have_1 = 0.20 * class_record_have + 80 * exam_have
        have_2 = 0.40 * class_record_have + 60 * exam_have

        if have_1 >= have_2:
            have = have_1
            lost = 0.20 * class_record_lost + 80 * exam_lost
        else:
            have = have_2
            lost = 0.40 * class_record_lost + 60 * exam_lost

    elif course == "phy2010s":
        course_grade_values = {"test": [0, 0, 20], "wps": [0, 0, 10], "lab": [0, 0, 20], "exam": [0, 0, 50]}
        wps_have, wps_lost, labs_have, labs_lost, tests_have, tests_lost, \
        exam_have, exam_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for (k, v) in course_marks:
            if v == "":
                continue

            if "test" in k:
                tests_have += eval(v)
                tests_lost += 1 - eval(v)
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "wps" in k:
                wps_have += eval(v)
                wps_lost += 1 - eval(v)
                course_grade_values["wps"][0] += 1
                course_grade_values["wps"][1] += eval(v)
            elif "lab" in k:
                labs_have += eval(v)
                labs_lost += 1 - eval(v)
                course_grade_values["lab"][0] += 1
                course_grade_values["lab"][1] += eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

        have = 20 * (tests_have / 2) + 10 * (wps_have / 10) + 20 * (labs_have / 3) + 50 * exam_have
        lost = 20 * (tests_lost / 2) + 10 * (wps_lost / 10) + 20 * (labs_lost / 3) + 50 * exam_lost

    # Third Year, first semester
    elif course == "csc2001f":
        course_grade_values = {"assignment": [0, 0, 33.3], "test": [0, 0, 16.7], "exam": [0, 0, 50]}
        assignments_have, assignments_lost, ct_have, ct_lost, exam_have, exam_lost = 0, 0, 0, 0, 0, 0

        for k, v in course_marks:
            if v == "":
                continue

            if "assignment" in k:
                assignments_have += eval(v)
                assignments_lost += 1 - eval(v)
                course_grade_values["assignment"][0] += 1
                course_grade_values["assignment"][1] += eval(v)
            elif "test" in k:
                ct_have += eval(v)
                ct_lost += 1 - eval(v)
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

        have = 33.3 * assignments_have / 6 + 16.7 * ct_have / 2 + 50 * exam_have
        lost = 33.3 * assignments_lost / 6 + 16.7 * ct_lost / 2 + 50 * exam_lost

    elif course == "eee3088f":
        course_grade_values = {"design_review": [0, 0, 1], "concept_proposal": [0, 0, 4], "design_proposal": [0, 0, 4],
                               "pcb": [0, 0, 4], "docs": [0, 0, 6.5], "initial": [0, 0, 6], "draft_report": [0, 0, 6],
                               "lab_demo": [0, 0, 8.5], "test": [0, 0, 10], "exam": [0, 0, 50]}
        design_review_have, design_review_lost = 0, 0

        for k, v in course_marks:
            if v == "":
                continue

            if "design_review" in k:
                design_review_have += eval(v)
                design_review_lost += 1 - eval(v)
                course_grade_values["design_review"][0] += 1
                course_grade_values["design_review"][1] += eval(v)
            elif k == "concept_proposal":
                have += 4 * eval(v)
                lost += 4 * (1 - eval(v))
                course_grade_values["concept_proposal"][0] += 1
                course_grade_values["concept_proposal"][1] += eval(v)
            elif k == "design_proposal":
                have += 4 * eval(v)
                lost += 4 * (1 - eval(v))
                course_grade_values["design_proposal"][0] += 1
                course_grade_values["design_proposal"][1] += eval(v)
            elif "pcb" in k:
                have += 4 * eval(v)
                lost += 4 * (1 - eval(v))
                course_grade_values["pcb"][0] += 1
                course_grade_values["pcb"][1] += eval(v)
            elif "docs" in k:
                have += 6.5 * eval(v)
                lost += 6.5 * (1 - eval(v))
                course_grade_values["docs"][0] += 1
                course_grade_values["docs"][1] += eval(v)
            elif "initial" in k:
                have += 6 * eval(v)
                lost += 6 * (1 - eval(v))
                course_grade_values["initial"][0] += 1
                course_grade_values["initial"][1] += eval(v)
            elif k == "draft_report":
                have += 6 * eval(v)
                lost += 6 * (1 - eval(v))
                course_grade_values["draft_report"][0] += 1
                course_grade_values["draft_report"][1] += eval(v)
            elif k == "lab_demo":
                have += 8.5 * eval(v)
                lost += 8.5 * (1 - eval(v))
                course_grade_values["lab_demo"][0] += 1
                course_grade_values["lab_demo"][1] += eval(v)
            elif "test" in k:
                have += 10 * eval(v)
                lost += 10 * (1 - eval(v))
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "exam" in k:
                have += 50 * eval(v)
                lost += 50 * (1 - eval(v))
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

        have += design_review_have / 8
        lost += design_review_lost / 8

    elif course == "eee3089f":
        for (k, v) in course_marks:
            if v == "":
                continue

    elif course == "eee3090f":
        course_grade_values = {"practical_test": [0, 0, 1], "assignment": [0, 0, 10], "practical": [0, 0, 5],
                               "test": [0, 0, 34], "exam": [0, 0, 50]}

        for (k, v) in course_marks:
            if v == "":
                continue

            if k == "practical_test":
                have += eval(v)
                lost += 1 - eval(v)
                course_grade_values["practical_test"][0] += 1
                course_grade_values["practical_test"][1] += eval(v)
            elif "assignment" in k:
                have += 2 * eval(v)
                lost += 2 * (1 - eval(v))
                course_grade_values["assignment"][0] += 1
                course_grade_values["assignment"][1] += eval(v)
            elif "practical" in k:
                have += eval(v)
                lost += 1 - eval(v)
                course_grade_values["practical"][0] += 1
                course_grade_values["practical"][1] += eval(v)
            elif "test" in k:
                have += 17 * eval(v)
                lost += 17 * (1 - eval(v))
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "exam" in k:
                have += 50 * eval(v)
                lost += 50 * (1 - eval(v))
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

    elif course == "eee3092f":
        course_grade_values = {"test": [0, 0, 20], "julia": [0, 0, 10], "lab": [0, 0, 5],
                               "exam": [0, 0, 65]}

        for (k, v) in course_marks:
            if v == "":
                continue

            if "test" in k:
                have += 10 * eval(v)
                lost += 10 * (1 - eval(v))
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "julia" in k:
                have += 10 / 3 * eval(v)
                lost += 10 / 3 * (1 - eval(v))
                course_grade_values["julia"][0] += 1
                course_grade_values["julia"][1] += eval(v)
            elif "lab" in k:
                have += 5 * eval(v)
                lost += 5 * (1 - eval(v))
                course_grade_values["lab"][0] += 1
                course_grade_values["lab"][1] += eval(v)
            elif "exam" in k:
                have += 65 * eval(v)
                lost += 65 * (1 - eval(v))
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

    # Third Year, Second Semester
    elif course == "csc2002s":
        course_grade_values = {"assignment": [0, 0, 33.3], "test": [0, 0, 16.7], "exam": [0, 0, 50]}
        assignments_have, assignments_lost, ct_have, ct_lost, exam_have, exam_lost = 0, 0, 0, 0, 0, 0

        for k, v in course_marks:
            if v == "":
                continue

            if any(substring in k for substring in ["pcp", "mdd", "arch"]):
                assignments_have += eval(v) if "mdd" not in k else (eval(v) * 0.8 if k == "mdd_1" else eval(v) * 1.2)
                assignments_lost += (1 - eval(v)) if "mdd" not in k else (round((0.8 - eval(v) * 0.8), 3) if k == "mdd_1" else round((1.2 - eval(v) * 1.2), 3))
                course_grade_values["assignment"][0] += 1
                course_grade_values["assignment"][1] += eval(v) if "mdd" not in k else (eval(v) * 0.8 if k == "mdd_1" else eval(v) * 1.2)
            elif "test" in k:
                ct_have += eval(v)
                ct_lost += 1 - eval(v)
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

        have = 33.3 * assignments_have / 5 + 16.7 * ct_have / 2 + 50 * exam_have
        lost = 33.3 * assignments_lost / 5 + 16.7 * ct_lost / 2 + 50 * exam_lost

    elif course == "eee3093s":
        course_grade_values = {"tutorial": [0, 0, 10], "lab": [0, 0, 10], "test": [0, 0, 20], "exam": [0, 0, 60]}
        tutorial_have, tutorial_lost, lab_have, lab_lost, test_have, test_lost, exam_have, exam_lost = 0, 0, 0, 0, 0, 0, 0, 0

        for k, v in course_marks:
            if v == "":
                continue

            if "tutorial" in k:
                tutorial_have += eval(v)
                tutorial_lost += 1 - eval(v)
                course_grade_values["tutorial"][0] += 1
                course_grade_values["tutorial"][1] += eval(v)
            elif "lab" in k:
                lab_have += eval(v)
                lab_lost += 1 - eval(v)
                course_grade_values["lab"][0] += 1
                course_grade_values["lab"][1] += eval(v)
            elif "test" in k:
                test_have += eval(v)
                test_lost += 1 - eval(v)
                course_grade_values["test"][0] += 1
                course_grade_values["test"][1] += eval(v)
            elif "exam" in k:
                exam_have += eval(v)
                exam_lost += 1 - eval(v)
                course_grade_values["exam"][0] += 1
                course_grade_values["exam"][1] += eval(v)

        have = 10 * tutorial_have / 8 + 10 * lab_have / 5 + 10 * test_have + 60 * exam_have
        lost = 10 * tutorial_lost / 8 + 10 * lab_lost / 5 + 10 * test_lost + 60 * exam_lost

    elif course == "eee3097s":
        course_grade_values = {"assignment": [0, 0, 45], "report": [0, 0, 55]}
        assignments_have, assignments_lost, report_have, report_lost = 0, 0, 0, 0

        for k, v in course_marks:
            if v == "":
                continue

            if any(substring in k for substring in ["design", "progress"]):
                assignments_have += eval(v)
                assignments_lost += 1 - eval(v)
                course_grade_values["assignment"][0] += 1
                course_grade_values["assignment"][1] += eval(v)
            elif "final" in k:
                report_have += eval(v)
                report_lost += 1 - eval(v)
                course_grade_values["report"][0] += 1
                course_grade_values["report"][1] += eval(v)

        have = 15 * assignments_have + 55 * report_have
        lost = 15 * assignments_lost + 55 * report_lost

    for values in course_grade_values.values():
        if values[0] != 0:
            course_grade += (values[1] / values[0]) * values[2]
            weighting += values[2]

    try:
        course_grade_calc = 100 * course_grade / weighting
    except ZeroDivisionError:
        course_grade_calc = 0

    return round(have, 3), round(lost, 3), round(course_grade_calc, 3)


def calculate_gpa():
    total_units = 0
    total_GP = [0, 0]  # [have, lost]
    units_by_year = {1: 0, 2: 0, 3: 0}  # {year: units}
    GP_by_year = {1: [0, 0], 2: [0, 0], 3: [0, 0]}  # {year: [have, lost]}
    GP_by_semester = {1: {1: [0, 0, 0], 2: [0, 0, 0]}, 2: {1: [0, 0, 0], 2: [0, 0, 0]},
                      3: {1: [0, 0, 0]}}  # {year: {semester: [have, lost, total_units]}}

    for year in range(1, 4):
        for j in range(0, len(courses_by_year[years[year]])):
            course = courses_by_year[years[year]][j]
            if course in ["csc2002s", "eee3093s", "eee3096s", "eee3097s"]:
                continue
            have, lost, units = float(data[years[year]][course]["have"]), float(
                data[years[year]][course]["lost"]), float(data[years[year]][course]["units"])

            total_units += units  # units for each course
            total_GP[0] += units * have  # grade-points have for each course
            total_GP[1] += units * lost  # grade-points lost for each course

            units_by_year[year] += units  # units for each course by year
            GP_by_year[year][0] += units * have  # grade-points awarded for each course by year
            GP_by_year[year][1] += units * lost  # grade-points lost for each course by year

            # TODO: change this when courses no longer follow a [F]irst semester, [S]econd semester structure.
            semester_num = 1 if course[-1] == "f" else 2
            GP_by_semester[year][semester_num][0] += units * have
            GP_by_semester[year][semester_num][1] += units * lost
            GP_by_semester[year][semester_num][2] += units

    return total_GP, total_units, units_by_year, GP_by_year, GP_by_semester


# WORK IN PROGRESS
def make_course_gp_graph():
    num_of_colors = len(data[years[1]]) + len(data[years[2]]) + len(data[years[3]])

    cm = plt.get_cmap('gist_rainbow')
    fig, ax = plt.subplots()
    ax.set_prop_cycle(color=[cm(1. * i / num_of_colors) for i in range(num_of_colors)])

    for ys, courses in list(courses_by_semester.items())[:-1]:
        year = eval(ys[1])

        for course in courses:
            course_values = [(k, v) for k, v in data[years[year]][course].items()]

            have = eval(course_values[0][1])
            lost = eval(course_values[1][1])
            units = eval(course_values[-1][1])

            ax.scatter(have * units, lost * units, label=course.upper())

    ax.legend(bbox_to_anchor=(1, 1.02), loc="upper left")
    ax.grid(True)
    ax.minorticks_on()
    plt.xlabel("Course GP")
    plt.ylabel("Course GP Lost")

    plt.tight_layout()
    plt.savefig("Reports/course_gps.png")
    # plt.show()


# WORK IN PROGRESS
def make_report_graphs():
    # TODO: - Complete this

    make_course_gp_graph()


# WORK IN PROGRESS
def make_reports():
    total_GP, total_units, units_by_year, GP_by_year, GP_by_semester = calculate_gpa()

    output = []

    for ys, courses in list(courses_by_semester.items())[:-1]:
        year = eval(ys[1])
        semester = eval(ys[3])

        for course in courses:
            course_values = [(k, v) for k, v in data[years[year]][course].items()]

            have = eval(course_values[0][1])
            lost = eval(course_values[1][1])
            units = eval(course_values[-1][1])

            output.append({"Course": course.upper(), "Year": year, "Semester": semester, "Have": have, "Lost": lost,
                           "Units": units, "Grade-Points": round(have * units, 3)})

    with open(file=f"Reports/course_report_{date.today()}.csv", mode="w") as course_report:
        course_report.write("Course,Year,Semester,Have,Lost,Units,Grade Points\n")

        for course_data in output:
            line = ""
            for k, v in course_data.items():
                line += (str(v) + ",") if list(course_data.keys()).index(k) != len(course_data.items()) - 1 else str(v)

            course_report.write(line + "\n")

    with open(file=f"Reports/GPA_report_{date.today()}.csv", mode="w") as gpa_report:

        # SEMESTER GPAs
        gpa_report.write("Year-Semester,Semester GPA,Semester GPA Lost,Semester GPA Remaining,Semester GPA Max\n")
        for year in range(1, 4):
            for semester in range(1, 3):
                # TODO: - Make this cleaner (skipping 2nd semester 3rd year)
                if semester == 2 and year == 3:
                    continue
                GP = GP_by_semester[year][semester]
                units = GP[2]
                gpa_have = GP[0] / units
                gpa_lost = GP[1] / units
                gpa_remaining = abs(100 - gpa_have - gpa_lost)
                gpa_max = 100 - gpa_lost

                gpa_report.write(f"{year}-{semester},{round(gpa_have, 3)},{round(gpa_lost, 3)},"
                                 f"{round(gpa_remaining, 3)},{round(gpa_max, 3)}\n")

        gpa_report.write(",\n")

        # YEAR GPAs
        gpa_report.write("Year,Year GPA,Year GPA Lost,Year GPA Remaining,Year GPA Max\n")
        for year in range(1, 3):
            gpa_have = GP_by_year[year][0] / units_by_year[year]
            gpa_lost = GP_by_year[year][1] / units_by_year[year]
            gpa_remaining = abs(100 - gpa_have - gpa_lost)
            gpa_max = 100 - gpa_lost

            gpa_report.write(f"{year},{round(gpa_have, 3)},{round(gpa_lost, 3)},"
                             f"{round(gpa_remaining, 3)},{round(gpa_max, 3)}\n")

        gpa_report.write(",\n")

        # Degree GPA
        gpa_report.write("Degree,Degree GPA,Degree GPA Lost,Degree GPA Remaining,Degree GPA Max\n")
        gpa_have = total_GP[0] / total_units
        gpa_lost = total_GP[1] / total_units
        gpa_remaining = abs(100 - gpa_have - gpa_lost)
        gpa_max = 100 - gpa_lost

        gpa_report.write(f",{round(gpa_have, 3)},{round(gpa_lost, 3)},{round(gpa_remaining, 3)},{round(gpa_max, 3)}\n")

    # messagebox.showinfo(title=None, message="Created progress reports successfully!")


# WORK IN PROGRESS
def create_reports():
    try:
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "/Reports")
        print("Created Reports Directory")
        make_reports()
        make_report_graphs()
    except OSError as os_error:
        if os_error.errno != 17:
            print(os_error)
        else:
            make_reports()
            make_report_graphs()


class Main(Tk):
    def __init__(self):
        super().__init__()
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        views = ["EmptyView", "CurrentMarks", "FirstYear", "SecondYear", "ThirdYear",
                 "MAM1020F", "CSC1015F", "PHY1012F", "EEE1006F", "MEC1003F",
                 "MAM1021S", "CSC1016S", "PHY1013S", "EEE1007S", "AXL1200S",
                 "EEE2045F", "EEE2046F", "EEE2048F", "MAM2083F", "MEC1009F",
                 "EEE2044S", "EEE2047S", "MAM2084S", "CON2026S", "PHY2010S",
                 "CSC2001F", "EEE3088F", "EEE3089F", "EEE3090F", "EEE3092F",
                 "CSC2002S", "EEE3093S", "EEE3094S", "EEE3096S", "EEE3097S"]

        for view in views:
            for F in (StartPage, eval(view)):
                frame = F(self.container, self)
                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.make_menu()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def make_menu(self):
        # Creates and adds the menu cascade for saving the current graph
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Create progress reports", command=lambda: create_reports())
        self.menubar.add_cascade(label="File", menu=file_menu)


class StartPage(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        titleLabel = Label(self, text="UCT Mark Calculator", font=("", 20))
        titleLabel.pack(pady=(10, 15), padx=10)

        button = Button(self, text=f"First Year\t\t\t>>>", command=lambda: view_controller.show_frame(FirstYear))
        button.pack(pady=3, padx=50)

        button = Button(self, text=f"Second Year\t\t>>>", command=lambda: view_controller.show_frame(SecondYear))
        button.pack(pady=3, padx=50)

        button = Button(self, text=f"Third Year\t\t\t>>>", command=lambda: view_controller.show_frame(ThirdYear))
        button.pack(pady=3, padx=50)

        button = Button(self, text="Current Marks for semester\t>>>",
                        command=lambda: (view_controller.show_frame(CurrentMarks)))
        button.pack(pady=10, padx=50)

        """GPALabel = Label(self, text="Grade-Point Averages", font=("", 20))
        GPALabel.pack(pady=(30, 2), padx=10)

        total_GP, total_units, units_by_year, GP_by_year, GP_by_semester = calculate_gpa()

        year = 3
        semester = 1

        semester_gpa_have = GP_by_semester[year][semester][0] / GP_by_semester[year][semester][2]
        semester_gpa_lost = GP_by_semester[year][semester][1] / GP_by_semester[year][semester][2]

        year_gpa_have = GP_by_year[year][0] / units_by_year[year]
        year_gpa_lost = GP_by_year[year][1] / units_by_year[year]

        degree_gpa_have = total_GP[0] / total_units
        degree_gpa_lost = total_GP[1] / total_units

        SemesterGPALabel = Label(self, text=f"Semester GPA have: {round(semester_gpa_have, 3)}\n"
                                            f"Year GPA lost: {round(semester_gpa_lost, 3)}\n"
                                            f"Semester GPA remaining: {round(100 - semester_gpa_have - semester_gpa_lost, 3)}\n"
                                            f"Semester GPA max: {round(100 - semester_gpa_lost, 3)}")
        SemesterGPALabel.pack(pady=(3, 2), padx=50)

        YearGPALabel = Label(self, text=f"Year GPA have: {round(year_gpa_have, 3)}\n"
                                        f"Year GPA lost: {round(year_gpa_lost, 3)}\n"
                                        f"Year GPA remaining: {round(100 - year_gpa_have - year_gpa_lost, 3)}\n"
                                        f"Year GPA max: {round(100 - year_gpa_lost, 3)}", font=("", 14))
        YearGPALabel.pack(pady=(3, 2), padx=50)

        CumulativeGPALabel = Label(self, text=f"Degree GPA have: {round(degree_gpa_have, 3)}\n"
                                              f"Degree GPA lost: {round(degree_gpa_lost, 3)}\n"
                                              f"Degree GPA max: {round(100 - degree_gpa_lost, 3)}", font=("", 14))
        CumulativeGPALabel.pack(pady=(3, 2), padx=50)"""

        # Adds a small buffer between the bottom of the homepage and the lowest button
        bottomBufferLabel = Label(self, text="")
        bottomBufferLabel.pack()


class FirstYear(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(StartPage))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="First Year", font=("", 20))
        titleLabel.grid(row=0, column=1, pady=18)

        button = Button(self, text="MAM1020F\t\t>>>", command=lambda: view_controller.show_frame(MAM1020F))
        button.grid(row=1, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="CSC1015F\t\t\t>>>", command=lambda: view_controller.show_frame(CSC1015F))
        button.grid(row=2, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="PHY1012F\t\t\t>>>", command=lambda: view_controller.show_frame(PHY1012F))
        button.grid(row=3, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE1006F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE1006F))
        button.grid(row=4, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="MEC1003F\t\t\t>>>", command=lambda: view_controller.show_frame(MEC1003F))
        button.grid(row=5, column=1, pady=(2, 15), padx=(0, 50))

        button = Button(self, text=f"MAM1021S\t\t>>>", command=lambda: view_controller.show_frame(MAM1021S))
        button.grid(row=6, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="CSC1016S\t\t\t>>>", command=lambda: view_controller.show_frame(CSC1016S))
        button.grid(row=7, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="PHY1013S\t\t\t>>>", command=lambda: view_controller.show_frame(PHY1013S))
        button.grid(row=8, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE1007S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE1007S))
        button.grid(row=9, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="AXL1200S\t\t\t>>>", command=lambda: view_controller.show_frame(AXL1200S))
        button.grid(row=10, column=1, pady=(2, 30), padx=(0, 50))


class SecondYear(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(StartPage))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Second Year", font=("", 20))
        titleLabel.grid(row=0, column=1, pady=18)

        button = Button(self, text="EEE2045F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2045F))
        button.grid(row=1, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE2046F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2046F))
        button.grid(row=2, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE2048F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2048F))
        button.grid(row=3, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="MAM2083F\t\t>>>", command=lambda: view_controller.show_frame(MAM2083F))
        button.grid(row=4, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="MEC1009F\t\t\t>>>", command=lambda: view_controller.show_frame(MEC1009F))
        button.grid(row=5, column=1, pady=(2, 15), padx=(0, 50))

        button = Button(self, text=f"CON2026S\t\t\t>>>", command=lambda: view_controller.show_frame(CON2026S))
        button.grid(row=6, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE2044S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2044S))
        button.grid(row=7, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE2047S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2047S))
        button.grid(row=8, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="MAM2084S\t\t>>>", command=lambda: view_controller.show_frame(MAM2084S))
        button.grid(row=9, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="PHY2010S\t\t\t>>>", command=lambda: view_controller.show_frame(PHY2010S))
        button.grid(row=10, column=1, pady=(2, 30), padx=(0, 50))


class ThirdYear(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(StartPage))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Third Year", font=("", 20))
        titleLabel.grid(row=0, column=1, pady=18)

        button = Button(self, text="CSC2001F\t\t\t>>>", command=lambda: view_controller.show_frame(CSC2001F))
        button.grid(row=1, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3088F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3088F))
        button.grid(row=2, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3089F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3089F))
        button.grid(row=3, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3090F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3090F))
        button.grid(row=4, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3092F\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3092F))
        button.grid(row=5, column=1, pady=(2, 15), padx=(0, 50))

        button = Button(self, text="CSC2002S\t\t\t>>>", command=lambda: view_controller.show_frame(CSC2002S))
        button.grid(row=6, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3093S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3093S))
        button.grid(row=7, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3094S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3094S))
        button.grid(row=8, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3096S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3096S))
        button.grid(row=9, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE3097S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE3097S))
        button.grid(row=10, column=1, pady=(2, 30), padx=(0, 50))


class CurrentMarks(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        if 1 <= date.today().month < 7:
            self.courses = ["csc2001f", "eee3088f", "eee3089f", "eee3090f", "eee3092f"]
        elif 7 <= date.today().month <= 12:
            self.courses = ["csc2002s", "eee3093s", "eee3096s", "eee3097s"]

        self.num_of_rows = len(self.courses) + 1

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="Current marks for the semester:", font=("", 15, "bold"))
        titleLabel.grid(row=0, column=1, pady=20, padx=(0, 20))

        self.add_grid()

    def add_grid(self):
        # TODO - Update label when the marks for a course change

        for i in range(1, self.num_of_rows):
            course = self.courses[i - 1]

            Label(self, text=course.upper() + ":", font=("", 15, "bold")).grid(row=i, sticky=N, padx=20)

            have, lost, units, course_grade = float(data[years[3]][course]["have"]), \
                                              float(data[years[3]][course]["lost"]), \
                                              float(data[years[3]][course]["units"]), \
                                              float(data[years[3]][course]["course_grade"])

            course_marks = Label(self, text=f"You currently have: {have}%\nYou have lost: {lost}%\n"
                                            f"Remaining marks: {round(100 - lost - have, 3)}%\n"
                                            f"Maximum marks: {round(100 - lost, 3)}%\n"
                                            f"Have/Lost: {round(have / lost, 3) if lost != 0 else 'NULL'}\n"
                                            f"Course Grade #1: {course_grade}%\n"
                                            f"Course Grade #2: {round(100 * have / (have + lost), 3) if (have + lost) != 0 else 'NULL'}%",
                                 font=("", 15))
            course_marks.grid(row=i, column=1, padx=(0, 20), pady=(0, 20))


class EmptyView(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)


class CourseTemplate(Frame):
    # TODO - Add red highlight when an input appears to be incorrect (e.g. 120/100 or 120%)

    def add_header(self, view_controller, name):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F, MEC1003F
        Varying for PHY1013S, PHY1012F, PHY2010S

        :param view_controller: class which is controlling the template
        :param name: course name (capitalized)
        :return: None
        """

        button = Button(self, text="<<< Back", command=lambda: view_controller
                        .show_frame(FirstYear if name.lower() in courses_by_year["first_year"]
                                    else (SecondYear if name.lower() in courses_by_year["second_year"]
                                          else ThirdYear)))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text=f"{name} Marks", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1 if height >= 1080 else (1 if ("PHY" not in name) else 3), pady=20)

    def add_grid(self, marks, rows, code):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F
        Varying for PHY1013S, PHY1012F, MEC1003F, PHY2010S

        :param marks: marks gathered from JSON document
        :param rows: number of rows required for the input of course results
        :param code: course code
        :return: None
        """

        for i in range(2, rows):
            assessmentName = marks[i - 2][0]

            if code == "mec1003f":
                labelText = assessmentName.replace('_', ' ').upper() + ':' if 'pcb' in assessmentName else \
                    assessmentName.replace('_', ' ').title() + ':'
            elif code == "phy1012f":
                labelText = assessmentName.replace('wps', 'WPS').replace('uct_lab_', 'UCT Lab ').replace('_', ' ') + ':' \
                    if any(substring in assessmentName for substring in ['wps', 'uct']) \
                    else assessmentName.replace('_', ' ').title() + ':'
            elif code == "phy1013s":
                labelText = assessmentName.replace('_', ' ').upper() + ':' \
                    if 'wps' in assessmentName else assessmentName.replace('_', ' ').title() + ':'
            elif code == "phy2010s":
                labelText = assessmentName.replace('_', ' ').upper() + ':' \
                    if 'wps' in assessmentName else assessmentName.replace('_', ' ').title() + ':'
            elif code == "eee2044s":
                labelText = assessmentName.replace('_', ' ').title().replace("Dc", "DC") + ':' \
                    if 'dc' in assessmentName else assessmentName.replace('_', ' ').title() + ':'
            elif code == "mam2084s":
                labelText = assessmentName.replace('_', ' ').title().replace("Webwork", "WebWork") + ':' \
                    if 'webwork' in assessmentName else assessmentName.replace('_', ' ').title() + ':'
            elif code == "csc2002s":
                labelText = assessmentName.replace('_', ' ').upper() + ':' \
                    if any(substring in assessmentName for substring in ["mdd", "pcp"]) else assessmentName.replace('_', ' ').title() + ':'
            else:
                labelText = assessmentName.replace("_", " ").title() + ":"

            assessmentLabel = Label(self, text=labelText)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify="right")
            entryText.set(marks[i - 2][1])

            if code in ["phy1012f", "phy2010s"] and (height < 1080 and i > 13):
                assessmentLabel.grid(row=i - 12, column=2, sticky=W, padx=20)
                assessmentEntry.grid(row=i - 12, column=3, padx=(0, 20))
            elif code == "phy1013s" and (height < 1080 and i > 12):
                assessmentLabel.grid(row=i - 11, column=2, sticky=W, padx=20)
                assessmentEntry.grid(row=i - 11, column=3, padx=(0, 20))
            else:
                assessmentLabel.grid(row=i, sticky=W, padx=20)
                assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def add_footer(self, rows, marks, year, code):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F, MEC1003F
        Varying for PHY1013S, PHY1012F, PHY2010S

        :param marks: marks gathered from JSON document
        :param rows: number of rows required for the input of course results
        :param year: year in which the course is taught
        :param code: course code
        :return: None
        """

        if "phy" in code:
            self.column_span = 2 if height >= 1080 else 4
        else:
            self.column_span = 2

        saveButton = Button(self, text="Save Marks",
                            command=lambda: self.get_inputs(marks=marks, rows=rows, year=year, code=code))
        saveButton.grid(row=rows + 1, column=0, columnspan=self.column_span, pady=30)

        results_section = Label(self, text="Results:", font=("", 18))
        results_section.grid(row=rows + 2, column=0, columnspan=self.column_span, pady=(30, 15))

        # Results Label
        year = years[year]
        have = float(data[year][code]["have"])
        lost = float(data[year][code]["lost"])
        course_grade = float(data[year][code]["course_grade"])
        self.previous_marks = Label(self, text=f"You currently have: {have}%\nYou have lost: {lost}%\n"
                                               f"Remaining marks: {round(100 - lost - have, 3)}%\n"
                                               f"Maximum marks: {round(100 - lost, 3)}%\n"
                                               f"Have/Lost: {round(have / lost, 3) if lost != 0 else 'NULL'}\n"
                                               f"Course Grade #1: {course_grade}%\n"
                                               f"Course Grade #2: {round(100 * have / (have + lost), 3) if (have + lost) != 0 else 'NULL'}%",
                                    font=("", 15))
        self.previous_marks.grid(row=rows + 3, column=0, columnspan=self.column_span, pady=(0, 30))

    def get_inputs(self, marks, rows, year, code):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F, MEC1003F
        *Varying for PHY1013S, PHY1012F, PHY2010S (*technically not, but whatever)

        :param marks: marks gathered from JSON document
        :param rows: number of rows required for the input of course results
        :param year: year in which the course is taught
        :param code: course code
        :return: None
        """

        assessmentName = iter([item[0] for item in marks])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == "Entry":
                try:
                    name = next(assessmentName)
                    data[year][code].update({name: child_widget.get()})
                    marks = [(k, v) for k, v in data[year][code].items()][2:]
                except StopIteration:
                    pass

        # Updated results label
        have, lost, course_grade = calculate_marks(code, marks[:-1])
        data[year][code].update({"have": str(have), "lost": str(lost), "course_grade": str(course_grade)})
        self.previous_marks.destroy()
        current_marks = Label(self, text=f"You currently have: {have}%\nYou have lost: {lost}%\n"
                                         f"Remaining marks: {round(100 - lost - have, 3)}%\n"
                                         f"Maximum marks: {round(100 - lost, 3)}%\n"
                                         f"Have/Lost: {round(have / lost, 3) if lost != 0 else 'NULL'}\n"
                                         f"Course Grade #1: {course_grade}%\n"
                                         f"Course Grade #2: {round(100 * have / (have + lost), 3) if lost != 0 else 'NULL'}%", font=("", 15))

        # if "phy" in code:
        current_marks.grid(row=rows + 3, column=0, columnspan=self.column_span, pady=(0, 30))
        # else:
        # current_marks.grid(row=rows + 3, column=0, columnspan=2, pady=(0, 30))


# First Semester, First Year {
class MAM1020F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mam1020f"
        year = 1

        self.add_header(view_controller, name="MAM1020F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class PHY1012F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "phy1012f"
        year = 1

        self.add_header(view_controller, name="PHY1012F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE1006F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee1006f"
        year = 1

        self.add_header(view_controller, name="EEE1006F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class CSC1015F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "csc1015f"
        year = 1

        self.add_header(view_controller, name="CSC1015F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MEC1003F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mec1003f"
        year = 1

        self.add_header(view_controller, name="MEC1003F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


# Second Semester, First Year {
class MAM1021S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mam1021s"
        year = 1

        self.add_header(view_controller, name="MAM1021S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(year=year, code=code, rows=rows, marks=marks)


class PHY1013S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "phy1013s"
        year = 1

        self.add_header(view_controller, name="PHY1013S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE1007S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee1007s"
        year = 1

        self.add_header(view_controller, name="EEE1007S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class CSC1016S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "csc1016s"
        year = 1

        self.add_header(view_controller, name="CSC1016S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class AXL1200S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "axl1200s"
        year = 1

        self.add_header(view_controller, name="AXL1200S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


# First Semester, Second Year {
class EEE2045F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2045f"
        year = 2

        self.add_header(view_controller, name="EEE2045F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE2046F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2046f"
        year = 2

        self.add_header(view_controller, name="EEE2046F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE2048F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2048f"
        year = 2

        self.add_header(view_controller, name="EEE2048F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MAM2083F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mam2083f"
        year = 2

        self.add_header(view_controller, name="MAM2083F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MEC1009F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mec1009f"
        year = 2

        self.add_header(view_controller, name="MEC1009F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


# Second Semester, Second Year {
class CON2026S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        """button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(SecondYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Awaiting Convenor", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)"""

        code = "con2026s"
        year = 2

        self.add_header(view_controller, name="CON2026S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE2044S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2044s"
        year = 2

        self.add_header(view_controller, name="EEE2044S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE2047S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2047s"
        year = 2

        self.add_header(view_controller, name="EEE2047S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MAM2084S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mam2084s"
        year = 2

        self.add_header(view_controller, name="MAM2084S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class PHY2010S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "phy2010s"
        year = 2

        self.add_header(view_controller, name="PHY2010S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


# First Semester, Third Year {
class CSC2001F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "csc2001f"
        year = 3

        self.add_header(view_controller, name="CSC2001F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE3088F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee3088f"
        year = 3

        self.add_header(view_controller, name="EEE3088F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE3089F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(ThirdYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "eee3089f"
        year = 3

        self.add_header(view_controller, name="EEE2089F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class EEE3090F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee3090f"
        year = 3

        self.add_header(view_controller, name="EEE3090F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE3092F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee3092f"
        year = 3

        self.add_header(view_controller, name="EEE3092F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


# Second Semester, Third Year {
class CSC2002S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "csc2002s"
        year = 3

        self.add_header(view_controller, name="CSC2002S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE3093S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        """button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(ThirdYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)"""

        code = "eee3093s"
        year = 3

        self.add_header(view_controller, name="EEE3093S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE3094S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(ThirdYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "eee3094s"
        year = 3

        self.add_header(view_controller, name="EEE3094S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class EEE3096S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(ThirdYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "eee3096s"
        year = 3

        self.add_header(view_controller, name="EEE3096S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class EEE3097S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee3097s"
        year = 3

        self.add_header(view_controller, name="EEE3097S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:-2]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


def start_up():
    with open("results.json", "r+") as json_file:
        json_data = json.load(json_file)
        data.update(json_data)

        # Updating for MAM2083F
        if data["meta"]["version"] == "2.00a":
            mam2083f = {}
            for i in range(1, 11):
                mam2083f.update({f"quiz_{i}": ""})

            mam2083f.update({"test_1": "", "test_2": "", "exam": ""})
            data["second_year"]["mam2083f"].update(mam2083f)
            data["meta"].update({"last_updated": str(date.today()), "version": "2.00b"})

        # Updating for EEE2048F
        if data["meta"]["version"] == "2.00b":
            eee2048f = {}
            for i in range(1, 5):
                eee2048f.update({f"practical_task_{i}": ""})

            eee2048f.update({"application_task": "", "academic_writing_task": "", "referencing_multiple_choice": "",
                             "report_critique": "", "capstone_proposal": "", "capstone_report": ""})
            data["second_year"]["eee2048f"].update(eee2048f)
            data["meta"].update({"last_updated": str(date.today()), "version": "2.00c"})

        # Updating for EEE2045F
        if data["meta"]["version"] == "2.00c":
            eee2045f = {}
            for i in range(1, 5):
                eee2045f.update({f"tutorial_test_{i}": ""})

            eee2045f.update(
                {"laboratory_1": "", "laboratory_2": "", "class_test_1": "", "class_test_2": "", "exam": ""})
            data["second_year"]["eee2045f"].update(eee2045f)
            data["meta"].update({"last_updated": str(date.today()), "version": "2.00d"})

        # Updating for EEE2046F
        if data["meta"]["version"] == "2.00d":
            eee2046f = {}
            for i in range(1, 5):
                eee2046f.update({f"practical_{i}": ""})

            eee2046f.update({"class_test_1": "", "class_test_2": "", "exam": ""})
            data["second_year"]["eee2046f"].update(eee2046f)
            data["meta"].update({"last_updated": str(date.today()), "version": "2.00e"})

        # Updating for MEC1009F
        if data["meta"]["version"] == "2.00e":
            mec1009f = {}
            for i in range(1, 8):
                mec1009f.update({f"tutorial_test_{i}": ""})

            for i in range(1, 4):
                mec1009f.update({f"class_test_{i}": ""})

            mec1009f.update({"exam": ""})

            data["second_year"]["mec1009f"].update(mec1009f)
            data["meta"].update({"last_updated": str(date.today()), "version": "2.00"})

        # Updating for EEE2045F
        if data["meta"]["version"] == "2.00":
            eee2045f = {}
            eee2045f.update({k: v for k, v in data["second_year"]["eee2045f"].items()
                             if list(data["second_year"]["eee2045f"].keys()).index(k) <= 5})
            eee2045f.update({"pre-practical_1": "", "pre-practical_2": ""})
            eee2045f.update({k: v for k, v in data["second_year"]["eee2045f"].items()
                             if list(data["second_year"]["eee2045f"].keys()).index(k) > 5})

            data["second_year"]["eee2045f"] = eee2045f
            data["meta"].update({"last_updated": str(date.today()), "version": "2.02"})

        # Updating for MAM2083F
        if data["meta"]["version"] == "2.02":
            mam2083f_temp = data["second_year"]["mam2083f"]
            mam2083f = mam2083f_temp.copy()
            for k, v in mam2083f_temp.items():
                if "quiz" in k and (k[-2] != "_" and eval(k[-2:]) > 10):
                    mam2083f.pop(k, None)

            data["second_year"]["mam2083f"] = mam2083f
            data["meta"].update({"last_updated": str(date.today()), "version": "2.04a"})

        # Updating for EEE2045F
        if data["meta"]["version"] == "2.04a":
            eee2045f = {}
            for (k, v) in data["second_year"]["eee2045f"].items():
                if k != "pre-practical_2" and k != "laboratory_2":
                    eee2045f.update({k: v})
                elif k == "pre-practical_2":
                    eee2045f.update({k: v, "pre-practical_3": ""})
                elif k == "laboratory_2":
                    eee2045f.update({k: v, "laboratory_3": ""})

            data["second_year"]["eee2045f"] = eee2045f
            data["meta"].update({"last_updated": str(date.today()), "version": "2.04"})

        # Adding/removing assessments which did not happen prior to exams
        if data["meta"]["version"] == "2.04":
            # MEC1009F Tutorial Test 7
            data["second_year"]["mec1009f"].pop("tutorial_test_7")

            # MAM2083F Tutorial total (lecturer calculated mark)
            mam2083f = {}
            for (k, v) in data["second_year"]["mam2083f"].items():
                mam2083f.update({k: v})
                if k == "quiz_10":
                    mam2083f.update({"tutorial_total": ""})

            data["second_year"]["mam2083f"] = mam2083f
            data["meta"].update({"last_updated": str(date.today()), "version": "2.05"})

        # Adding 2nd Semester course assessments (excl. CON2026S)
        if data["meta"]["version"] == "2.05":
            # EEE2044S
            eee2044s = data["second_year"]["eee2044s"]

            eee2044s.update({"transformer_lab": "", "dc_machines_lab": "", "project_task_1": "",
                             "project_task_2": "", "class_test_1": "", "class_test_2": "", "exam": ""})

            data["second_year"]["eee2044s"].update(eee2044s)

            # EEE2047S
            eee2047s = data["second_year"]["eee2047s"]

            eee2047s.update({"problem_set_1": "", "problem_set_2": "", "problem_set_3": "",
                             "lab_1": "", "lab_2": "", "lab_3": "", "class_test": "", "exam": ""})

            data["second_year"]["eee2047s"].update(eee2047s)

            # MAM2084S
            mam2084s = data["second_year"]["mam2084s"]

            for i in range(1, 7):
                mam2084s.update({f"webwork_test_{i}": ""})

            mam2084s.update({"class_test_1": "", "class_test_2": "", "exam": ""})

            data["second_year"]["mam2084s"].update(mam2084s)

            # PHY2010S
            phy2010s = data["second_year"]["phy2010s"]

            for i in range(1, 13):
                phy2010s.update({f"wps_{i}": ""})

            for i in range(1, 4):
                phy2010s.update({f"lab_{i}": ""})

            phy2010s.update({"class_test_1": "", "class_test_2": "", "class_test_3": "", "exam": ""})

            data["second_year"]["phy2010s"].update(phy2010s)

            data["meta"].update({"last_updated": str(date.today()), "version": "2.06"})

        # Adding GPA field
        if data["meta"]["version"] == "2.06":
            # First Year
            data["first_year"]["mam1020f"].update({"units": "18"})
            data["first_year"]["phy1012f"].update({"units": "18"})
            data["first_year"]["eee1006f"].update({"units": "12"})
            data["first_year"]["csc1015f"].update({"units": "18"})
            data["first_year"]["mec1003f"].update({"units": "8"})

            data["first_year"]["mam1021s"].update({"units": "18"})
            data["first_year"]["phy1013s"].update({"units": "18"})
            data["first_year"]["eee1007s"].update({"units": "12"})
            data["first_year"]["csc1016s"].update({"units": "18"})
            data["first_year"]["axl1200s"].update({"units": "8"})

            # Second Year
            data["second_year"]["eee2045f"].update({"units": "16"})
            data["second_year"]["eee2046f"].update({"units": "16"})
            data["second_year"]["eee2048f"].update({"units": "8"})
            data["second_year"]["mam2083f"].update({"units": "16"})
            data["second_year"]["mec1009f"].update({"units": "16"})

            data["second_year"]["con2026s"].update({"units": "16"})  # Incorrect
            data["second_year"]["eee2044s"].update({"units": "16"})
            data["second_year"]["eee2047s"].update({"units": "16"})
            data["second_year"]["mam2084s"].update({"units": "8"})  # Incorrect
            data["second_year"]["phy2010s"].update({"units": "16"})

            data["meta"].update({"last_updated": str(date.today()), "version": "2.08"})

        # Useless code...
        if data["meta"]["version"] == "2.08":
            con2026s = data["second_year"]["con2026s"]

            con2026s.pop("units")

            for module in range(1, 11):
                con2026s.update(
                    {f"assignment_{module}.A1": "", f"assignment_{module}.A2": ""} if module not in [2, 5] else {
                        f"assignment_{module}.A1": ""})

            con2026s.update({"main_assignment": "", "class_test": "", "final_exam": "", "units": "16"})

            data["second_year"]["con2026s"].update(con2026s)
            data["meta"].update({"last_updated": str(date.today()), "version": "2.09"})

        # Fixing CON2026S and MAM2084S units
        # Adding most of the CON2026S assignments
        if data["meta"]["version"] == "2.09":
            data["second_year"]["con2026s"].update({"units": "8"})
            data["second_year"]["mam2084s"].update({"units": "16"})

            con2026s = data["second_year"]["con2026s"]

            last_4_keys = {"main_assignment": con2026s["main_assignment"], "class_test": con2026s["class_test"],
                           "final_exam": con2026s["final_exam"], "units": "8"}

            temp_con2026s = {"have": 0, "lost": 0, "1.A1_eskom_procurement": "", "1.A2_team_roles": "",
                             "2.A1_scope_statement": "", "3.A1_design_thinking": "", "3.A2_project_planning": "",
                             "4.A1_cost_estimate": "", "4.A2_tracking_costs": "", "5.A1_handing_over_projects": "",
                             "6.A1_indirect_procurement": "", "7.A1_stakeholder_management": "",
                             "8.A1_risk_identification": ""}

            temp_con2026s.update(last_4_keys)

            data["second_year"]["con2026s"] = temp_con2026s
            data["meta"].update({"last_updated": str(date.today()), "version": "2.10"})

        # Removing CT3 from PHY2010S
        if data["meta"]["version"] == "2.10":
            phy2010s = data["second_year"]["phy2010s"]
            phy2010s.pop("class_test_3")

            data["second_year"]["phy2010s"] = phy2010s
            data["meta"].update({"last_updated": str(date.today()), "version": "2.11"})

        if data["meta"]["version"] == "2.11":
            con2026s = data["second_year"]["con2026s"]

            last_4_keys = {"main_assignment": con2026s["main_assignment"], "class_test": con2026s["class_test"],
                           "final_exam": con2026s["final_exam"], "units": "8"}

            temp_con2026s = {k: con2026s[k] for k in [k for k in con2026s.keys() if k not in last_4_keys.keys()]}
            temp_con2026s.update({"10.A1_communication_exercise": ""})
            temp_con2026s.update(last_4_keys)

            data["second_year"]["con2026s"] = temp_con2026s
            data["meta"].update({"last_updated": str(date.today()), "version": "2.12"})

        if data["meta"]["version"] == "2.12":
            mam2084s = data["second_year"]["mam2084s"]
            mam2084s.pop("webwork_test_6")
            data["second_year"]["mam2084s"] = mam2084s

            phy2010s = data["second_year"]["phy2010s"]
            phy2010s.pop("wps_11")
            phy2010s.pop("wps_12")
            data["second_year"]["phy2010s"] = phy2010s

            data["meta"].update({"last_updated": str(date.today()), "version": "2.13"})

        # Updating for third year
        if data["meta"]["version"] == "2.13":
            data["third_year"].update({"csc2001f": {}, "eee3088f": {}, "eee3089f": {}, "eee3090f": {}, "eee3092f": {}})

            csc2001f = {"have": "0", "lost": "0"}
            for i in range(1, 7):
                csc2001f.update({f"assignment_{i}": ""})

            csc2001f.update({"test_1": "", "test_2": "", "exam": "", "units": "24"})
            data["third_year"]["csc2001f"].update(csc2001f)

            eee3088f = {"have": "0", "lost": "0", "design_review_wk3": "", "design_review_wk4": "",
                        "design_review_wk5": "",
                        "design_review_wk7": "", "design_review_wk8": "", "design_review_wk10": "",
                        "concept_proposal": "", "design_proposal": "", "initial_design": "", "draft_pcb_design": "",
                        "gerbers": "", "draft_report": "", "docs_&_software": "", "lab_demo": "",
                        "test": "", "exam": "", "units": "8"}
            data["third_year"]["eee3088f"].update(eee3088f)

            eee3089f = {"have": "0", "lost": "0", "units": "16"}
            data["third_year"]["eee3089f"].update(eee3089f)

            eee3090f = {"have": "0", "lost": "0", "practical_assignment_1": "", "practical_assignment_2": "",
                        "practical_assignment_3": "",
                        "practical_assignment_4": "", "practical_assignment_5": "",
                        "practical_1": "", "practical_2": "", "practical_3": "", "practical_4": "", "practical_5": "",
                        "practical_test": "", "test_1": "", "test_2": "", "exam": "", "units": "16"}
            data["third_year"]["eee3090f"].update(eee3090f)

            eee3092f = {"have": "0", "lost": "0", "julia_assignment_1": "", "julia_assignment_2": "",
                        "julia_assignment_3": "",
                        "julia_assignment_4": "", "lab_1": "", "lab_2": "", "test_1": "", "test_2": "", "exam": "",
                        "units": "16"}
            data["third_year"]["eee3092f"].update(eee3092f)

            data["meta"].update({"last_updated": str(date.today()), "version": "2.14"})

        # Updating for course grades
        if data["meta"]["version"] == "2.14":
            # First Year
            data["first_year"]["mam1020f"].update({"course_grade": "0"})
            data["first_year"]["phy1012f"].update({"course_grade": "0"})
            data["first_year"]["eee1006f"].update({"course_grade": "0"})
            data["first_year"]["csc1015f"].update({"course_grade": "0"})
            data["first_year"]["mec1003f"].update({"course_grade": "0"})

            data["first_year"]["mam1021s"].update({"course_grade": "0"})
            data["first_year"]["phy1013s"].update({"course_grade": "0"})
            data["first_year"]["eee1007s"].update({"course_grade": "0"})
            data["first_year"]["csc1016s"].update({"course_grade": "0"})
            data["first_year"]["axl1200s"].update({"course_grade": "0"})

            # Second Year
            data["second_year"]["eee2045f"].update({"course_grade": "0"})
            data["second_year"]["eee2046f"].update({"course_grade": "0"})
            data["second_year"]["eee2048f"].update({"course_grade": "0"})
            data["second_year"]["mam2083f"].update({"course_grade": "0"})
            data["second_year"]["mec1009f"].update({"course_grade": "0"})

            data["second_year"]["con2026s"].update({"course_grade": "0"})
            data["second_year"]["eee2044s"].update({"course_grade": "0"})
            data["second_year"]["eee2047s"].update({"course_grade": "0"})
            data["second_year"]["mam2084s"].update({"course_grade": "0"})
            data["second_year"]["phy2010s"].update({"course_grade": "0"})

            # Third Year
            data["third_year"]["csc2001f"].update({"course_grade": "0"})
            data["third_year"]["eee3088f"].update({"course_grade": "0"})
            data["third_year"]["eee3089f"].update({"course_grade": "0"})
            data["third_year"]["eee3090f"].update({"course_grade": "0"})
            data["third_year"]["eee3092f"].update({"course_grade": "0"})

            data["meta"].update({"last_updated": str(date.today()), "version": "2.15"})

        # Updating EEE3092F for simulation assignments and labs
        if data["meta"]["version"] == "2.15":
            eee3092f = data["third_year"]["eee3092f"]
            eee3092f.pop("julia_assignment_4")
            eee3092f.pop("lab_2")

            data["third_year"]["eee3092f"] = eee3092f
            data["meta"].update({"last_updated": str(date.today()), "version": "2.16"})

        # Updating EEE3088F for gerbers
        if data["meta"]["version"] == "2.16":
            eee3088f = data["third_year"]["eee3088f"]
            eee3088f.pop("gerbers")

            data["third_year"]["eee3088f"] = eee3088f
            data["meta"].update({"last_updated": str(date.today()), "version": "2.17"})

        # Updating for assignments not being done
        if data["meta"]["version"] == "2.17":
            eee3092f = data["third_year"]["eee3092f"]
            eee3092f.pop("julia_assignment_3")
            data["third_year"]["eee3092f"] = eee3092f

            eee3088f = data["third_year"]["eee3088f"]
            eee3088f_new = {}
            for k, v in eee3088f.items():
                if k != "design_review_wk10":
                    eee3088f_new.update({k: v})
                else:
                    eee3088f_new.update({"design_review_wk10": "", "design_review_wk12": "", "design_review_wk13": ""})
            data["third_year"]["eee3088f"] = eee3088f_new

            data["meta"].update({"last_updated": str(date.today()), "version": "2.18"})

        # Re-adding EEE3092F assignment 3
        if data["meta"]["version"] == "2.18":
            eee3092f = data["third_year"]["eee3092f"]
            eee3092f_new = {}
            for k, v in eee3092f.items():
                if k == "julia_assignment_2":
                    eee3092f_new.update({k: v, "julia_assignment_3": ""})
                else:
                    eee3092f_new.update({k: v})

            data["third_year"]["eee3092f"] = eee3092f_new
            data["meta"].update({"last_updated": str(date.today()), "version": "2.19"})

        # Adding 3rd year 2nd semester courses
        if data["meta"]["version"] == "2.19":
            data["third_year"].update({"csc2002s": {}, "eee3093s": {}, "eee3094s": {}, "eee3096s": {}, "eee3097s": {}})

            csc2002s = {"have": "0", "lost": "0", "pcp_1": "", "pcp_2": "", "mdd_1": "", "mdd_2": "", "arch_1": "",
                        "class_test_1": "", "class_test_2": "", "exam": "", "units": "24", "course_grade": "0"}
            data["third_year"]["csc2002s"].update(csc2002s)

            eee3093s = {"have": "0", "lost": "0", "tutorial_1": "", "tutorial_2": "", "tutorial_3": "",
                        "tutorial_4": "", "tutorial_5": "", "tutorial_6": "", "tutorial_7": "", "tutorial_8": "",
                        "lab_1": "", "lab_2": "", "lab_3": "", "lab_4": "", "lab_5": "", "test_1": "", "test_2": "",
                        "exam": "", "units": "16", "course_grade": "0"}
            data["third_year"]["eee3093s"].update(eee3093s)

            eee3094s = {"have": "0", "lost": "0", "units": "16", "course_grade": "0"}
            data["third_year"]["eee3094s"].update(eee3094s)

            eee3096s = {"have": "0", "lost": "0", "units": "16", "course_grade": "0"}
            data["third_year"]["eee3096s"].update(eee3096s)

            eee3097s = {"have": "0", "lost": "0", "paper_design": "", "progress_report_1": "", "progress_report_2": "",
                        "final_report": "", "units": "8", "course_grade": "0"}
            data["third_year"]["eee3097s"].update(eee3097s)

            data["meta"].update({"last_updated": str(date.today()), "version": "2.20"})

        app = Main()

        if errors:
            message = ""
            if "pyautogui" in errors:
                message += "If your screens resolution is less than 1080p, please install pyautogui with \"pip3 install pyautogui\""
                errors.remove('pyautogui')

            if ("matplotlib" in errors) or ("numpy" in errors):
                num_of_errors = len(errors)
                module_text = f"Please install {errors[0]}" + (f" and {errors[1]}" if num_of_errors == 2 else "")
                message += ("\n\n" if message else "") + f"{module_text} with \"pip3 install <module name>\" in " \
                                                         f"order for the generation of the mark reports to work " \
                                                         f"to its full potential."

            messagebox.showwarning(title=None, message=message)

        def on_closing():
            app.destroy()
            json_file.seek(0)  # move cursor to beginning of file
            json.dump(data, json_file, indent=4)
            json_file.truncate()

        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()


def main():
    try:
        start_up()
    except FileNotFoundError:
        with open("results.json", "w") as json_file:
            data.update({
                "meta": {
                    "last_updated": str(date.today()),
                    "version": "2.00a"
                },
                "grade_point_averages": {
                    "first_year": 0,
                    "second_year": 0,
                    "third_year": 0,
                    "fourth_year": 0,
                    "degree_gpa": 0
                },
                "first_year": {
                    "mam1020f": {
                        "have": 0,
                        "lost": 0
                    },
                    "phy1012f": {
                        "have": 0,
                        "lost": 0
                    },
                    "eee1006f": {
                        "have": 0,
                        "lost": 0
                    },
                    "csc1015f": {
                        "have": 0,
                        "lost": 0
                    },
                    "mec1003f": {
                        "have": 0,
                        "lost": 0
                    },
                    "mam1021s": {
                        "have": 0,
                        "lost": 0
                    },
                    "phy1013s": {
                        "have": 0,
                        "lost": 0
                    },
                    "csc1016s": {
                        "have": 0,
                        "lost": 0
                    },
                    "eee1007s": {
                        "have": 0,
                        "lost": 0
                    },
                    "axl1200s": {
                        "have": 0,
                        "lost": 0
                    }
                },
                "second_year": {
                    "eee2045f": {
                        "have": 0,
                        "lost": 0
                    },
                    "eee2046f": {
                        "have": 0,
                        "lost": 0
                    },
                    "eee2048f": {
                        "have": 0,
                        "lost": 0
                    },
                    "mam2083f": {
                        "have": 0,
                        "lost": 0
                    },
                    "mec1009f": {
                        "have": 0,
                        "lost": 0
                    },
                    "con2026s": {
                        "have": 0,
                        "lost": 0
                    },
                    "eee2044s": {
                        "have": 0,
                        "lost": 0
                    },
                    "eee2047s": {
                        "have": 0,
                        "lost": 0
                    },
                    "mam2084s": {
                        "have": 0,
                        "lost": 0
                    },
                    "phy2010s": {
                        "have": 0,
                        "lost": 0
                    }
                },
                "third_year": {

                },
                "fourth_year": {

                }
            })

            with open("results.txt", "r") as old_txt:
                lines = old_txt.readlines()
                for line in lines[1:]:
                    course_code = line[:line.find("_")]
                    course_event = line[line.find("_") + 1: line.find(":")]
                    event_mark = line[line.rfind(":") + 1:].rstrip()
                    data["first_year"][course_code].update({course_event: event_mark})

            for course in ["mam1020f", "phy1012f", "eee1006f", "csc1015f", "mec1003f",
                           "mam1021s", "phy1013s", "csc1016s", "eee1007s", "axl1200s"]:
                marks = [(k, v) for k, v in data["first_year"][course].items()][2:]
                have, lost = calculate_marks(course, marks)
                data["first_year"][course].update({"have": str(have), "lost": str(lost)})

            json.dump(data, json_file, indent=4)

        start_up()


if __name__ == "__main__":
    main()
