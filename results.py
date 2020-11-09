#  Copyright (c) 2020 David Young.
#  All rights reserved
#

# v1.06

"""
THIS PROGRAM ONLY TAKES INTO ACCOUNT YOUR FINAL MARK... NOT WHETHER YOU GET DP
Try not to edit the results.txt file once it has been created... this may cause an unexpected error.
If you do encounter an error please let me know so that I can fix the problem.

BEWARE: There is very little input error checking in this version of the program
        So please try and input your marks either in decimal or quotient format (i.e. 0.96 or 24/25)
        If you only have the percentage value, please divide that value by 100 (convert to decimal)

I think that's all, lemme know if there's anything I need to explain about the program and I'll happily do so :)
Good luck
"""

from os.path import exists
from tkinter import *
from tkinter import messagebox

results = {}


def get_results(f):
    with open(f, mode='r') as file:
        filesLines = file.readlines()
        mam1020f, phy1012f, eee1006f, csc1015f, mec1003f, mam1021s, phy1013s, csc1016s, eee1007s, axl1200s \
            = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

        for line in filesLines[1:]:
            courseName = line[:8]
            mark = line.rstrip()[line.find(':') + 1:]
            assessment = line.rstrip()[:line.find(':')]

            eval(courseName).update({assessment: mark})

            if 'TBA' not in mark:
                results.update({assessment: mark[5:]})

    return mam1020f, phy1012f, eee1006f, csc1015f, mec1003f, mam1021s, phy1013s, csc1016s, eee1007s, axl1200s


def write_results(results):
    lines = open(results_file, mode='r').readlines()
    with open(results_file, mode='w') as file:

        for line in lines[1:]:
            for k, v in results.items():
                if line[:line.find(':')] == k and v != '':
                    lines[lines.index(line)] = f'{k}:DONE:{v}\n'
                    break
                elif line[:line.find(':')] == k and v == '':
                    lines[lines.index(line)] = f'{k}:TBA:0\n'
                    break

        file.writelines(lines)


def calculate_marks(results, course, user_run=False):
    have, lost = 0, 0

    quizzes_have, quizzes_lost, assignment_have, assignment_lost, practical_have, practical_lost, theory_have, \
    theory_lost, wps_have, wps_lost, lab_test_have, lab_test_lost, labs_have, labs_lost, class_tests_have, \
    class_tests_lost, reflection_have, reflection_lost, research_have, research_lost \
        = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    if course == 'mam1020f':
        # Case 1:
        test_count, final_test_have, final_test_lost, test_have, test_lost = 0, 0, 0, 0, 0
        tests = []

        for k, v in results.items():
            if 'mam1020f' in k:
                if 'class' in k:
                    class_tests_have += eval(v)
                    class_tests_lost += 1 - eval(v)
                elif 'final' in k:
                    final_test_have += eval(v)
                    final_test_lost += 1 - eval(v)
                elif 'test' in k:
                    tests.append([k, v])
                    test_count += 1
                    if test_count == 4:
                        tests.sort(key=lambda l: l[1], reverse=True)
                        for test in tests[:3]:
                            test_have += eval(test[1])
                            test_lost += 1 - eval(test[1])

        have = 25 * class_tests_have + 15 * test_have + 30 * final_test_have
        lost = 25 * class_tests_lost + 15 * test_lost + 30 * final_test_lost

    elif course == 'eee1006f':
        for k, v in results.items():
            if 'eee1006f' in k:
                if 'test' in k:
                    have += 25 * eval(v)
                    lost += 25 * (1 - eval(v))
                else:
                    have += 50 * eval(v)
                    lost += 50 * (1 - eval(v))

    elif course == 'phy1012f':
        first_test_have = 0
        first_test_lost = 0
        for k, v in results.items():
            if v != '' and course in k:
                if 'test_1' in k:
                    first_test_have += eval(v)
                    first_test_lost += 1 - eval(v)
                elif 'lab_test' in k:
                    lab_test_have += eval(v)
                    lab_test_lost += 1 - eval(v)
                elif 'test' in k:
                    class_tests_have += eval(v)
                    class_tests_lost += 1 - eval(v)
                elif 'wps' in k:
                    wps_have += eval(v)
                    wps_lost += 1 - eval(v)
                elif 'lab' in k:
                    labs_have += eval(v)
                    labs_lost += 1 - eval(v)

        have = 30 * first_test_have + 10 * class_tests_have + \
               10 * (wps_have / 14) + 15 * (labs_have / 4) + 15 * lab_test_have
        lost = 30 * first_test_lost + 10 * class_tests_lost + \
               10 * (wps_lost / 14) + 15 * (labs_lost / 4) + 15 * lab_test_lost
        
    else:
        for k, v in results.items():
            if v != '' and course in k:
                if 'quiz' in k:
                    quizzes_have += eval(v)
                    quizzes_lost += 1 - eval(v)
                elif 'practical_test' in k:
                    practical_have += eval(v)
                    practical_lost += 1 - eval(v)
                elif 'theory' in k:
                    theory_have += eval(v)
                    theory_lost += 1 - eval(v)
                elif 'test_' in k and course == 'mam1021s':
                    have += eval(v) * 20
                    lost += (1 - eval(v)) * 20
                elif 'test_' in k:
                    class_tests_have += eval(v)
                    class_tests_lost += 1 - eval(v)
                elif 'final' in k:
                    have += eval(v) * 25
                    lost += (1 - eval(v)) * 25
                elif 'assignment' in k:
                    assignment_have += eval(v)
                    assignment_lost += 1 - eval(v)
                elif 'wps' in k:
                    wps_have += eval(v)
                    wps_lost += 1 - eval(v)
                elif 'lab_test' in k:
                    lab_test_have = eval(v) * 7.5
                    lab_test_lost = (1 - eval(v)) * 7.5
                elif 'lab' in k:
                    labs_have += eval(v)
                    labs_lost += 1 - eval(v)
                elif 'reflection' in k:
                    reflection_have += eval(v)
                    reflection_lost += 1 - eval(v)
                elif 'research_project' in k:
                    have += eval(v) * 30
                    lost += (1 - eval(v)) * 30
                elif 'application' in k:
                    have += eval(v) * 55
                    lost += (1 - eval(v)) * 55
                elif 'gerber' in k:
                    have += eval(v) * 20
                    lost += (1 - eval(v)) * 20
                elif 'pcb' in k:
                    have += eval(v) * 15
                    lost += (1 - eval(v)) * 15
                elif 'schematic' in k:
                    have += eval(v) * 10
                    lost += (1 - eval(v)) * 10

        if course == 'csc1016s':
            practical_average_have = 0.9 * (assignment_have / 6) + 0.1 * (quizzes_have / 7)
            practical_average_lost = 0.9 * (assignment_lost / 6) + 0.1 * (quizzes_lost / 7)
            have += practical_average_have * 36 + 24 * (practical_have / 2) + 40 * (theory_have / 3)
            lost += practical_average_lost * 36 + 24 * (practical_lost / 2) + 40 * (theory_lost / 3)

        elif course == 'mam1021s':
            have += (quizzes_have * 15) / 10
            lost += (quizzes_lost * 15) / 10

        elif course == 'phy1013s':
            wps_have = 10 * (wps_have / 12)
            wps_lost = 10 * (wps_lost / 12)

            have += wps_have + lab_test_have + 7.5 * (labs_have / 4) + 75 * (class_tests_have / 4)
            lost += wps_lost + lab_test_lost + 7.5 * (labs_lost / 4) + 75 * (class_tests_lost / 4)

        elif course == 'eee1007s':
            have = class_tests_have * 35 + assignment_have * 30
            lost = class_tests_lost * 35 + assignment_lost * 30

        elif course == 'axl1200s':
            have += 70 * (reflection_have / 7) + 30 * research_have
            lost += 70 * (reflection_lost / 7) + 30 * research_lost

        elif course == 'csc1015f':
            practical_avg_have = 0.6 * (0.1 * (quizzes_have / 7) + 0.9 * (assignment_have / 7)) + 0.4 * (
                    practical_have / 2)
            practical_avg_lost = 0.6 * (0.1 * (quizzes_lost / 7) + 0.9 * (assignment_lost / 7)) + 0.4 * (
                    practical_lost / 2)
            have = 100 * (0.625 * practical_avg_have + 0.375 * (theory_have / 3))
            lost = 100 * (0.625 * practical_avg_lost + 0.375 * (theory_lost / 3))

    if user_run:
        write_results(results)

    return round(have, 3), round(lost, 3)


class Main(Tk):
    def __init__(self):
        super().__init__()
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        courses = ["MAM1021S", "CSC1016S", "PHY1013S", "EEE1007S", "AXL1200S",
                   "MAM1020F", "CSC1015F", "PHY1012F", "EEE1006F", "MEC1003F", "CurrentMarks"]

        for course in courses:
            for F in (StartPage, eval(course)):
                frame = F(container, self)
                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_results(self, f):
        with open(f, mode='r') as file:
            filesLines = file.readlines()
            mam1020f, phy1012f, eee1006f, csc1015f, mec1003f, mam1021s, phy1013s, csc1016s, eee1007s, axl1200s \
                = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

            for line in filesLines[1:]:
                courseName = line[:8]
                mark = line.rstrip()[line.find(':') + 1:]
                assessment = line.rstrip()[:line.find(':')]

                eval(courseName).update({assessment: mark})

                if 'TBA' not in mark:
                    results.update({assessment: mark[5:]})

        return mam1020f, phy1012f, eee1006f, csc1015f, mec1003f, mam1021s, phy1013s, csc1016s, eee1007s, axl1200s


class StartPage(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        titleLabel = Label(self, text="UCT Mark Calculator", font=('', 20))
        titleLabel.pack(pady=10, padx=10)

        # Each of these calls a respective courses view
        button = Button(self, text=f"MAM1021S                                "
                                   f">>>", command=lambda: viewController.show_frame(MAM1021S))
        button.pack(pady=2, padx=50)

        button = Button(self, text="CSC1016S                                "
                                   ">>>", command=lambda: viewController.show_frame(CSC1016S))
        button.pack(pady=2, padx=50)

        button = Button(self, text="PHY1013S                                "
                                   ">>>", command=lambda: viewController.show_frame(PHY1013S))
        button.pack(pady=2, padx=50)

        button = Button(self, text="EEE1007S                                "
                                   ">>>", command=lambda: viewController.show_frame(EEE1007S))
        button.pack(pady=2, padx=50)

        button = Button(self, text="AXL1200S                                "
                                   ">>>", command=lambda: viewController.show_frame(AXL1200S))
        button.pack(pady=(2, 15), padx=50)

        button = Button(self, text="MAM1020F                                "
                                   ">>>", command=lambda: viewController.show_frame(MAM1020F))
        button.pack(pady=2, padx=50)

        button = Button(self, text="CSC1015F                                "
                                   ">>>", command=lambda: viewController.show_frame(CSC1015F))
        button.pack(pady=2, padx=50)

        button = Button(self, text="PHY1012F                                "
                                   ">>>", command=lambda: viewController.show_frame(PHY1012F))
        button.pack(pady=2, padx=50)

        button = Button(self, text="EEE1006F                                "
                                   ">>>", command=lambda: viewController.show_frame(EEE1006F))
        button.pack(pady=2, padx=50)

        button = Button(self, text="MEC1003F                                "
                                   ">>>", command=lambda: viewController.show_frame(MEC1003F))
        button.pack(pady=(2, 15), padx=50)

        button = Button(self, text="Current Marks for semester    "
                                   ">>>", command=lambda: (viewController.show_frame(CurrentMarks)))
        button.pack(pady=2, padx=50)

        # Adds a small buffer between the bottom of the homepage and the lowest button
        bottomBufferLabel = Label(self, text='')
        bottomBufferLabel.pack()


class MAM1021S(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.mam1021s_list = [(k, v) for k, v in mam1021s.items()]
        self.num_of_rows = len(self.mam1021s_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="MAM1021S Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'mam1021s')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.mam1021s_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.mam1021s_list[i - 2][1] else self.mam1021s_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.mam1021s_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'mam1021s', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class CSC1016S(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.csc1016s_list = [(k, v) for k, v in csc1016s.items()]
        self.num_of_rows = len(self.csc1016s_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="CSC1016S Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'csc1016s')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.csc1016s_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, column=0, sticky=W, padx=20)
                #.grid(row=i if i <= 13 else i - 12, column=0 if i <= 13 else 2, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.csc1016s_list[i - 2][1] else self.csc1016s_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.csc1016s_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'csc1016s', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class PHY1013S(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.phy1013s_list = [(k, v) for k, v in phy1013s.items()]
        self.num_of_rows = len(self.phy1013s_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="PHY1013S Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'phy1013s')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.phy1013s_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', '').upper() + ':' if 'wps' in assessmentName else
            assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.phy1013s_list[i - 2][1] else self.phy1013s_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.phy1013s_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'phy1013s', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class EEE1007S(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.eee1007s_list = [(k, v) for k, v in eee1007s.items()]
        self.num_of_rows = len(self.eee1007s_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="EEE1007S Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'eee1007s')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.eee1007s_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', '').upper() + ':' if 'wps' in assessmentName else
            assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.eee1007s_list[i - 2][1] else self.eee1007s_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.eee1007s_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'eee1007s', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class AXL1200S(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.axl1200s_list = [(k, v) for k, v in axl1200s.items()]
        self.num_of_rows = len(self.axl1200s_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="AXL1200S Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'axl1200s')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.axl1200s_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.axl1200s_list[i - 2][1] else self.axl1200s_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.axl1200s_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'axl1200s', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class MAM1020F(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.mam1020f_list = [(k, v) for k, v in mam1020f.items()]
        self.num_of_rows = len(self.mam1020f_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="MAM1020F Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'mam1020f')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.mam1020f_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.mam1020f_list[i - 2][1] else self.mam1020f_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.mam1020f_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'mam1020f', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class CSC1015F(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.csc1015f_list = [(k, v) for k, v in csc1015f.items()]
        self.num_of_rows = len(self.csc1015f_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="CSC1015F Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'csc1015f')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.csc1015f_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.csc1015f_list[i - 2][1] else self.csc1015f_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.csc1015f_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'csc1015f', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class PHY1012F(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.phy1012f_list = [(k, v) for k, v in phy1012f.items()]
        self.num_of_rows = len(self.phy1012f_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="PHY1012F Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'phy1012f')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.phy1012f_list[i - 2][0]

            Label(self,
                  text=assessmentName[9:].replace('wps', 'WPS').replace('uct_lab_', 'UCT Lab ').replace('_', '') + ':'
                  if any(substring in assessmentName for substring in ['wps', 'uct']) else
                  assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.phy1012f_list[i - 2][1] else self.phy1012f_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.phy1012f_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'phy1012f', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class EEE1006F(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.eee1006f_list = [(k, v) for k, v in eee1006f.items()]
        self.num_of_rows = len(self.eee1006f_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="EEE1006F Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'eee1006f')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.eee1006f_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.eee1006f_list[i - 2][1] else self.eee1006f_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.eee1006f_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'eee1006f', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class MEC1003F(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.mec1003f_list = [(k, v) for k, v in mec1003f.items()]
        self.num_of_rows = len(self.mec1003f_list) + 2

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="MEC1003F Mark Calculator", font=('', 15))
        titleLabel.grid(row=0, column=1, pady=20)

        self.add_grid()

        saveButton = Button(self, text="Save Marks", command=lambda: self.get_inputs())
        saveButton.grid(row=self.num_of_rows + 1, column=0, columnspan=2, pady=30)

        results_section = Label(self, text='Results:', font=('', 18))
        results_section.grid(row=self.num_of_rows + 2, column=0, columnspan=2, pady=(30, 15))

        # Results Label
        have, lost = calculate_marks(results, 'mec1003f')
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))

    def add_grid(self):
        # Rows
        for i in range(2, self.num_of_rows):
            assessmentName = self.mec1003f_list[i - 2][0]

            Label(self, text=assessmentName[9:].replace('_', ' ').upper() + ':' if 'pcb' in assessmentName else
            assessmentName[9:].replace('_', ' ').title() + ':').grid(row=i, sticky=W, padx=20)

            entryText = StringVar()
            assessmentEntry = Entry(self, textvariable=entryText, justify='right')
            entryText.set('' if 'TBA' in self.mec1003f_list[i - 2][1] else self.mec1003f_list[i - 2][1][5:])
            assessmentEntry.grid(row=i, column=1, padx=(0, 20))

    def get_inputs(self):
        assessmentName = iter([item[0] for item in self.mec1003f_list])

        children_widgets = Frame.winfo_children(self)
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                try:
                    name = next(assessmentName)
                    results.update({name: child_widget.get()})
                except StopIteration:
                    pass

        # Updated results label
        have, lost = calculate_marks(results, 'mec1003f', True)
        current_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                         f'Remaining marks: {round(100 - lost - have, 3)}%', font=('', 15))
        current_marks.grid(row=self.num_of_rows + 3, column=0, columnspan=2, pady=(0, 30))


class CurrentMarks(Frame):
    def __init__(self, parent, viewController):
        Frame.__init__(self, parent)

        self.courses = ['mam1021s', 'phy1013s', 'csc1016s', 'eee1007s', 'axl1200s']
        self.num_of_rows = len(self.courses) + 1

        button = Button(self, text="<<< Back", command=lambda: viewController.show_frame(StartPage))
        button.grid(row=0, column=0)

        titleLabel = Label(self, text="Current Marks For The Semester:", font=('', 15, 'bold'))
        titleLabel.grid(row=0, column=1, pady=20, padx=(0, 20))

        self.add_grid()

    def add_grid(self):
        # Rows
        for i in range(1, self.num_of_rows):
            course_name = self.courses[i - 1]

            Label(self, text=course_name.upper() + ':', font=('', 15, 'bold')).grid(row=i, sticky=N, padx=20)

            have, lost = calculate_marks(results, course_name)

            course_marks = Label(self, text=f'You currently have: {have}%\nYou have lost: {lost}%\n'
                                            f'Remaining marks: {round(100 - lost - have, 3)}%',
                                 font=('', 15), justify='left')
            course_marks.grid(row=i, column=1, padx=(0, 20), pady=(0, 20))


if __name__ == '__main__':
    results_file = 'results.txt'

    if exists(results_file):
        mam1020f, phy1012f, eee1006f, csc1015f, mec1003f, mam1021s, phy1013s, csc1016s, eee1007s, axl1200s \
            = get_results(results_file)

        app = Main()

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                app.destroy()
                write_results(results)

        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()

    else:
        warning = messagebox.askokcancel('OK',
                                         'You must run the make_results_file.py '
                                         'program first before running this program.\n'
                                         'OR\nRename results_example.txt to results.txt.')


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
