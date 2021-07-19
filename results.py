#  Copyright (c) 2021 David Young.
#  All rights reserved
#

# v2.06

from datetime import date
import json
from tkinter import *
from tkinter import messagebox

try:
    import pyautogui

    width, height = pyautogui.size()
    error = None
except ModuleNotFoundError as e:
    error = e
    height = 1080
    pass

data = {}
years = {1: "first_year", 2: "second_year", 3: "third_year", 4: "fourth_year"}
courses_by_year = {"first_year": ["mam1020f", "phy1012f", "eee1006f", "csc1015f", "mec1003f",
                                  "mam1021s", "phy1013s", "csc1016s", "eee1007s", "axl1200s"],
                   "second_year": ["eee2045f", "eee2046f", "eee2048f", "mam2083f", "mec1009f",
                                   "eee2044s", "eee2047s", "mam2084s", "con2026s", "phy2010s"]}


def calculate_marks(course, course_marks):
    have, lost = 0, 0

    # First Year, first semester
    if course == "mam1020f":
        # Case 1:
        test_count, final_test_have, final_test_lost, test_have, test_lost, class_tests_have, class_tests_lost = 0, 0, 0, 0, 0, 0, 0
        tests = []

        for (k, v) in course_marks:
            if v == "":
                continue

            if "class" in k:
                class_tests_have += eval(v)
                class_tests_lost += 1 - eval(v)
            elif "final" in k:
                final_test_have += eval(v)
                final_test_lost += 1 - eval(v)
            elif "test" in k:
                tests.append([k, v])
                test_count += 1
                if test_count == 4:
                    tests.sort(key=lambda l: l[1], reverse=True)
                    for test in tests[:3]:
                        test_have += eval(test[1])
                        test_lost += 1 - eval(test[1])

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

    return round(have, 3), round(lost, 3)


class Main(Tk):
    def __init__(self):
        super().__init__()
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        views = ["EmptyView", "CurrentMarks", "FirstYear", "SecondYear",
                 "MAM1020F", "CSC1015F", "PHY1012F", "EEE1006F", "MEC1003F",
                 "MAM1021S", "CSC1016S", "PHY1013S", "EEE1007S", "AXL1200S",
                 "EEE2045F", "EEE2046F", "EEE2048F", "MAM2083F", "MEC1009F",
                 "EEE2044S", "EEE2047S", "MAM2084S", "CON2026S", "PHY2010S"]

        for view in views:
            for F in (StartPage, eval(view)):
                frame = F(self.container, self)
                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        titleLabel = Label(self, text="UCT Mark Calculator", font=("", 20))
        titleLabel.pack(pady=(10, 15), padx=10)

        button = Button(self, text=f"First Year\t\t\t>>>", command=lambda: view_controller.show_frame(FirstYear))
        button.pack(pady=3, padx=50)

        button = Button(self, text=f"Second Year\t\t>>>", command=lambda: view_controller.show_frame(SecondYear))
        button.pack(pady=3, padx=50)

        button = Button(self, text="Current Marks for semester\t>>>",
                        command=lambda: (view_controller.show_frame(CurrentMarks)))
        button.pack(pady=10, padx=50)

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

        button = Button(self, text="EEE2044S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2044S))
        button.grid(row=7, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="EEE2047S\t\t\t>>>", command=lambda: view_controller.show_frame(EEE2047S))
        button.grid(row=8, column=1, pady=2, padx=(0, 50))

        button = Button(self, text=f"CON2026S\t\t\t>>>", command=lambda: view_controller.show_frame(CON2026S))
        button.grid(row=6, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="MAM2084S\t\t>>>", command=lambda: view_controller.show_frame(MAM2084S))
        button.grid(row=9, column=1, pady=2, padx=(0, 50))

        button = Button(self, text="PHY2010S\t\t\t>>>", command=lambda: view_controller.show_frame(PHY2010S))
        button.grid(row=10, column=1, pady=(2, 30), padx=(0, 50))


class CourseTemplate(Frame):
    # TODO - Add red highlight when an input appears to be incorrect (e.g. 120/100 or 120%)

    def add_header(self, view_controller, name):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F, MEC1003F
        Varying for PHY1013S, PHY1012F

        :param view_controller: class which is controlling the template
        :param name: course name (capitalized)
        :return: None
        """

        button = Button(self, text="<<< Back", command=lambda: view_controller
                        .show_frame(FirstYear if name.lower() in courses_by_year["first_year"] else SecondYear))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text=f"{name} Marks", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1 if height >= 1080 else (1 if ("PHY" not in name) else 3), pady=20)

    def add_grid(self, marks, rows, code):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F
        Varying for PHY1013S, PHY1012F, MEC1003F

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
                labelText = assessmentName.replace('wps', 'WPS').replace('uct_lab_', 'UCT Lab ').replace('_', '') + ':' \
                    if any(substring in assessmentName for substring in ['wps', 'uct']) \
                    else assessmentName.replace('_', ' ').title() + ':'
            elif code == "phy1013s":
                labelText = assessmentName.replace('_', '').upper() + ':' \
                    if 'wps' in assessmentName else assessmentName.replace('_', ' ').title() + ':'
            else:
                labelText = assessmentName.replace("_", " ").title() + ":"

            assessmentLabel = Label(self, text=labelText)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify="right")
            entryText.set(marks[i - 2][1])

            if code == "phy1012f" and (height < 1080 and i > 13):
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
        Varying for PHY1013S, PHY1012F

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
        self.previous_marks = Label(self, text=f"You currently have: {have}%\nYou have lost: {lost}%\n"
                                               f"Remaining marks: {round(100 - lost - have, 3)}%\n"
                                               f"Maximum marks: {round(100 - lost, 3)}%", font=("", 15))
        self.previous_marks.grid(row=rows + 3, column=0, columnspan=self.column_span, pady=(0, 30))

    def get_inputs(self, marks, rows, year, code):
        """
        Unvarying for MAM1021S, CSC1016S, EEE1007S, AXL1200S, MAM1020F, CSC1015F, EEE1006F, MEC1003F
        Varying for PHY1013S, PHY1012F

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
        have, lost = calculate_marks(code, marks)
        data[year][code].update({"have": str(have), "lost": str(lost)})
        self.previous_marks.destroy()
        current_marks = Label(self, text=f"You currently have: {have}%\nYou have lost: {lost}%\n"
                                         f"Remaining marks: {round(100 - lost - have, 3)}%\n"
                                         f"Maximum marks: {round(100 - lost, 3)}%", font=("", 15))

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

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class PHY1012F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "phy1012f"
        year = 1

        self.add_header(view_controller, name="PHY1012F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE1006F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee1006f"
        year = 1

        self.add_header(view_controller, name="EEE1006F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class CSC1015F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "csc1015f"
        year = 1

        self.add_header(view_controller, name="CSC1015F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MEC1003F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mec1003f"
        year = 1

        self.add_header(view_controller, name="MEC1003F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
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

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(year=year, code=code, rows=rows, marks=marks)


class PHY1013S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "phy1013s"
        year = 1

        self.add_header(view_controller, name="PHY1013S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE1007S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee1007s"
        year = 1

        self.add_header(view_controller, name="EEE1007S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class CSC1016S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "csc1016s"
        year = 1

        self.add_header(view_controller, name="CSC1016S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class AXL1200S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "axl1200s"
        year = 1

        self.add_header(view_controller, name="AXL1200S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
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

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE2046F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2046f"
        year = 2

        self.add_header(view_controller, name="EEE2046F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class EEE2048F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "eee2048f"
        year = 2

        self.add_header(view_controller, name="EEE2048F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MAM2083F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mam2083f"
        year = 2

        self.add_header(view_controller, name="MAM2083F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


class MEC1009F(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        code = "mec1009f"
        year = 2

        self.add_header(view_controller, name="MEC1009F")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)


# }


# Second Semester, Second Year {
class EEE2044S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(SecondYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "eee2044s"
        year = 2

        self.add_header(view_controller, name="EEE2044S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class EEE2047S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(SecondYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "eee2047s"
        year = 2

        self.add_header(view_controller, name="EEE2047S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class MAM2084S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(SecondYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "mam2084s"
        year = 2

        self.add_header(view_controller, name="MAM2084S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class CON2026S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(SecondYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "con2026s"
        year = 2

        self.add_header(view_controller, name="CON2026S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


class PHY2010S(CourseTemplate):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        button = Button(self, text="<<< Back", command=lambda: view_controller.show_frame(SecondYear))
        button.grid(row=0, column=0, padx=(34, 0))

        titleLabel = Label(self, text="Coming Soon", font=("", 15))
        titleLabel.grid(row=0, column=1, columnspan=1, pady=20, padx=10)

        """code = "phy2010s"
        year = 2

        self.add_header(view_controller, name="PHY2010S")

        marks = [(k, v) for k, v in data[years[year]][code].items()][2:]
        rows = len(marks) + 2

        self.add_grid(marks=marks, rows=rows, code=code)

        self.add_footer(rows=rows, marks=marks, year=year, code=code)"""


# }


class CurrentMarks(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)

        if 1 <= date.today().month < 8:
            self.courses = ["eee2045f", "eee2046f", "eee2048f", "mam2083f", "mec1009f"]
        elif 8 <= date.today().month <= 12:
            self.courses = ["con2026s", "eee2044s", "eee2047s", "mam2084s", "phy2010s"]

        # self.courses = ["mam1020f", "phy1012f", "csc1015f", "eee1006f", "mec1003f"]

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

            have, lost = float(data[years[2]][course]["have"]), float(data[years[2]][course]["lost"])

            course_marks = Label(self, text=f"You currently have: {have}%\nYou have lost: {lost}%\n"
                                            f"Remaining marks: {round(100 - lost - have, 3)}%\n"
                                            f"Maximum marks: {round(100 - lost, 3)}%", font=("", 15))
            course_marks.grid(row=i, column=1, padx=(0, 20), pady=(0, 20))


class EmptyView(Frame):
    def __init__(self, parent, view_controller):
        Frame.__init__(self, parent)


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

        app = Main()

        if error is not None:
            messagebox.showwarning(title=None, message="If your screen's pixel height is less than 1080, "
                                                       "please install pyautogui with \"pip3 install pyautogui\"")

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
