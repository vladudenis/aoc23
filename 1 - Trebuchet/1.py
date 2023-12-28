# Trebuchet

"""
PART 1
Problem:
The newly-improved calibration document consists of lines of text; each line originally contained a specific
calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining
the first digit and the last digit (in that order) to form a single two-digit number.

Goal: Recover calibration values.
"""


def recover_calibration_val(line: str):
    length = len(line)
    first_num, last_num = None, None

    for idx in range(length):
        if first_num is not None and last_num is not None:
            return int(first_num + "" + last_num)
        else:
            if first_num is None and line[idx].isnumeric():
                first_num = line[idx]
            if last_num is None and line[length - idx - 1].isnumeric():
                last_num = line[length - idx - 1]

    return int(first_num + "" + last_num)


def compute_val_sum(path_to_file, func):
    num_sum = 0
    with open(path_to_file, "r") as f:
        lines = f.readlines()

        for l in lines:
            recovered_val = func(l)
            num_sum += int(recovered_val)

    return num_sum


print(compute_val_sum("1_input.txt", recover_calibration_val))
# Answer: 54450

"""
PART 2
Problem:
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: 
one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Goal: Equipped with this new information, recover all calibration values.
"""


def recover_calibration_val_fr(line: str):
    line_length = len(line)
    first_num, last_num = None, None
    digit_letters = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    for idx in range(line_length):
        if first_num is not None and last_num is not None:
            return int(first_num + "" + last_num)
        else:
            if first_num is None:
                if line[idx].isnumeric():
                    first_num = line[idx]
                if idx >= 3:
                    for digit in digit_letters:
                        digit_length = len(digit)
                        if digit_length <= idx + 1 and line[idx - digit_length:idx] == digit:
                            first_num = str(int(digit_letters.index(digit)) + 1)
            if last_num is None:
                if line[line_length - idx - 1].isnumeric():
                    last_num = line[line_length - idx - 1]
                if idx >= 3:
                    for digit in digit_letters:
                        digit_length = len(digit)
                        if (digit_length <= idx + 1 and
                                line[line_length - idx - 1:line_length - idx + digit_length - 1] == digit):
                            last_num = str(int(digit_letters.index(digit)) + 1)

    return int(first_num + "" + last_num)


print(compute_val_sum("1_input.txt", recover_calibration_val_fr))
# Answer: 54265
