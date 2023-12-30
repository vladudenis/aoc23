# Gear Ratios

"""
PART 1
Problem:
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one.
If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine.
There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol,
even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Goal: What is the sum of all the part numbers in the engine schematic?
"""
import re
from math import prod


def is_schematic_symbol(char: str):
    return char and not char.isdigit() and char != "."


def get_part_numbers_line_sum(line: str, line_abv: str = None, line_blw: str = None):
    line_length = len(line)
    nums = re.findall("[0-9]+", line)
    nums_indices = []

    for idx, char in enumerate(line):
        prev_char = line[idx - 1] if idx != 0 else None
        next_char = line[idx - 1] if idx != line_length - 1 else None

        if char.isdigit() and (prev_char is None or not prev_char.isdigit()) and (
                next_char is None or not next_char.isdigit()):
            nums_indices.append(idx)

    if len(nums) != len(nums_indices):
        raise Exception()

    part_nums = []

    for i, num in enumerate(nums):
        n_num = int(num)
        num_idx = nums_indices[i]
        num_length = len(num)

        side_left_idx = num_idx - 1 if num_idx - 1 >= 0 else None
        side_right_idx = num_idx + num_length if num_idx + num_length < line_length - 1 else None

        if (side_left_idx and is_schematic_symbol(line[side_left_idx])) or (
                side_right_idx and is_schematic_symbol(line[side_right_idx])):
            part_nums.append(n_num)
            continue

        start_idx = num_idx - 1 if num_idx != 0 else num_idx
        end_idx = num_idx + num_length if num_idx + num_length < line_length - 1 else num_idx + num_length - 1

        for idx in range(start_idx, end_idx + 1):
            if (line_abv and is_schematic_symbol(line_abv[idx])) or (line_blw and is_schematic_symbol(line_blw[idx])):
                part_nums.append(n_num)
                break

    return sum(part_nums)


def get_part_numbers_sum():
    with open("3_input.txt", "r") as f:
        schematic = f.readlines()
        num_lines = len(schematic)
        parts_sum = 0

        for i, l in enumerate(schematic):
            if i == 0 and num_lines > 1:
                parts_sum += get_part_numbers_line_sum(l, line_blw=schematic[i + 1])
            elif i == num_lines - 1:
                parts_sum += get_part_numbers_line_sum(l, line_abv=schematic[i - 1])
            else:
                parts_sum += get_part_numbers_line_sum(l, line_abv=schematic[i - 1], line_blw=schematic[i + 1])

        return parts_sum


print(get_part_numbers_sum())
# Answer: 560670

"""
PART 2
Problem:
The missing part wasn't the only issue - one of the gears in the engine is wrong. 
A gear is any * symbol that is adjacent to exactly two part numbers. 
Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out 
which gear needs to be replaced.

Goal: What is the sum of all of the gear ratios in your engine schematic?
"""


def get_number_on_same_line(idx: int, line: str, leftwards: bool = False, rightwards: bool = False):
    parsed_num = ""

    if leftwards:
        for i in range(idx, -1, -1):
            if not line[i].isdigit():
                break
            parsed_num += line[i]
    elif rightwards:
        for i in range(idx, len(line)):
            if not line[i].isdigit():
                break
            parsed_num += line[i]

    if parsed_num == "":
        return None

    return int(parsed_num) if rightwards else int(parsed_num[::-1])


def get_numbers_on_other_line(idx: int, line: str):
    if line[idx].isdigit():
        first_idx = 0

        for i in range(idx, -1, -1):
            if not line[i].isdigit():
                first_idx = i + 1
                break

        return [get_number_on_same_line(first_idx, line, rightwards=True)]
    else:
        nums = []

        num_left = get_number_on_same_line(idx - 1 if idx - 1 >= 0 else idx, line, leftwards=True)
        num_right = get_number_on_same_line(idx + 1 if idx + 1 < len(line) - 1 else idx, line, rightwards=True)

        if num_left:
            nums.append(num_left)

        if num_right:
            nums.append(num_right)

        return nums


def get_gear_ratios_line_sum(line: str, line_abv: str = None, line_blw: str = None):
    line_length = len(line)
    star_indices = []
    gears = []

    for idx, char in enumerate(line):
        if char == "*":
            star_indices.append(idx)

    for i in star_indices:
        adjacents = []
        side_left_idx = i - 1 if i - 1 >= 0 else None
        side_right_idx = i + 1 if i + 1 < line_length - 1 else None

        if side_left_idx and line[side_left_idx].isdigit():
            adjacents.append(get_number_on_same_line(side_left_idx, line, leftwards=True))
        if side_right_idx and line[side_right_idx].isdigit():
            adjacents.append(get_number_on_same_line(side_right_idx, line, rightwards=True))
        if len(adjacents) == 2:
            gears.append(prod(adjacents))
            continue

        if line_abv:
            adjacents += get_numbers_on_other_line(i, line_abv)
        if len(adjacents) == 2:
            gears.append(prod(adjacents))
            continue

        if line_blw:
            adjacents += get_numbers_on_other_line(i, line_blw)
        if len(adjacents) == 2:
            gears.append(prod(adjacents))
            continue

    return sum(gears)


def get_gear_ratios_sum():
    with open("3_input.txt", "r") as f:
        schematic = f.readlines()
        num_lines = len(schematic)
        gear_ratio_sum = 0

        for i, l in enumerate(schematic):
            if i == 0 and num_lines > 1:
                gear_ratio_sum += get_gear_ratios_line_sum(l, line_blw=schematic[i + 1])
            elif i == num_lines - 1:
                gear_ratio_sum += get_gear_ratios_line_sum(l, line_abv=schematic[i - 1])
            else:
                gear_ratio_sum += get_gear_ratios_line_sum(l, line_abv=schematic[i - 1], line_blw=schematic[i + 1])

        return gear_ratio_sum


print(get_gear_ratios_sum())
# Answer: 91622824
