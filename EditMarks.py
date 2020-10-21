#  Copyright (c) 2020 David Young.
#  All rights reserved
#


def csc1016s_quizzes():
    lines = []
    with open("results.txt", "r") as openfile:
        temp_lines = openfile.readlines()

        for line in temp_lines:
            if "csc1016s_quiz_" in line and eval(line[line.rfind("_") + 1:line.find(":")]) > 7:
                pass
            else:
                lines.append(line)

    with open("results.txt", "w") as writefile:
        writefile.writelines(lines)


if __name__ == '__main__':
    # 21 Oct 2020
    csc1016s_quizzes()
