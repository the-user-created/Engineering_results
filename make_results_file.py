import os


def adjustForSecondSemester(f):
    with open(f, mode='r') as file:
        lines = file.readlines()

        if 'ADJUSTED\n' not in lines:
            lines.insert(0, 'ADJUSTED\n')
            os.remove('results.txt')
            new_file = open('results.txt', 'w')

            courses = ['mam1020f', 'phy1012f', 'eee1006f', 'csc1015f', 'mec1003f']

            for line in lines:
                if any(substring in line for substring in courses):
                    lines[lines.index(line)] = ''
                elif 'mam' in line:
                    lines[lines.index(line)] = line.replace('mam', 'mam1020f')
                elif 'phy' in line:
                    lines[lines.index(line)] = line.replace('phy', 'phy1012f')
                elif 'eee' in line:
                    lines[lines.index(line)] = line.replace('eee', 'eee1006f')
                elif 'csc' in line:
                    lines[lines.index(line)] = line.replace('csc', 'csc1015f')
                elif 'mec' in line:
                    lines[lines.index(line)] = line.replace('mec', 'mec1003f')

            lines = [line for line in lines if line]

            for i in range(1, 10):
                lines.append(f'mam1021s_quiz_{i}:TBA:0\n')

            lines += ['mam1021s_test_1:TBA:0\n', 'mam1021s_test_2:TBA:0\n', 'mam1021s_test_3:TBA:0\n',
                      'mam1021s_final_test:TBA:0\n']

            for i in range(1, 13):
                lines.append(f'phy1013s_wps_{i}:TBA:0\n')

            lines += ['phy1013s_lab_1:TBA:0\n', 'phy1013s_lab_2:TBA:0\n', 'phy1013s_lab_3:TBA:0\n',
                      'phy1013s_lab_4:TBA:0\n', 'phy1013s_lab_test:TBA:0\n', 'phy1013s_test_1:TBA:0\n',
                      'phy1013s_test_2:TBA:0\n', 'phy1013s_test_3:TBA:0\n', 'phy1013s_test_4:TBA:0\n']

            for i in range(1, 13):
                lines.append(f'csc1016s_quiz_{i}:TBA:0\n')

            lines += ['csc1016s_practical_test_1:TBA:0\n', 'csc1016s_practical_test_2:TBA:0\n',
                      'csc1016s_theory_test_1:TBA:0\n', 'csc1016s_theory_test_2:TBA:0\n',
                      'csc1016s_theory_test_3:TBA:0\n']

            for i in range(1, 7):
                lines.append(f'csc1016s_assignment_{i}:TBA:0\n')

            lines += ['eee1007s_test_1:TBA:0\n', 'eee1007s_test_2:TBA:0\n', 'eee1007s_assignment:TBA:0\n']

            for i in range(1, 8):
                lines.append(f'axl1200s_reflection_piece_{i}:TBA:0\n')

            lines += ['axl1200s_research_project:TBA:0\n']

            new_file.writelines(lines)
        else:
            print("You've already run this program")


if __name__ == '__main__':
    adjustForSecondSemester('results.txt')
