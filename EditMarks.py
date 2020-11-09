#  Copyright (c) 2020 David Young.
#  All rights reserved
#


def csc1016s_quizzes(file):
    lines = []
    with open(file, "r") as openfile:
        temp_lines = openfile.readlines()

        for line in temp_lines:
            if "csc1016s_quiz_" in line and eval(line[line.rfind("_") + 1:line.find(":")]) > 7:
                pass
            else:
                lines.append(line)

    with open(file, "w") as writefile:
        writefile.writelines(lines)


def mam1021s_quizzes(file):
    lines = []
    with open(file, "r") as openfile:
        temp_lines = openfile.readlines()

        for line in temp_lines:
            if "mam1021s_quiz_" in line and eval(line[line.rfind("_") + 1:line.find(":")]) == 9:
                lines.append(line)
                lines.append("mam1021s_quiz_10:TBA:0\n") if "mam1021s_quiz_10" not in temp_lines[temp_lines.index(line) + 1] else None
            else:
                lines.append(line)

    with open(file, "w") as writefile:
        writefile.writelines(lines)


if __name__ == '__main__':
    # 21 Oct 2020
    csc1016s_quizzes(file="results.txt")
    # 09 Nov 2020
    mam1021s_quizzes(file="results.txt")
