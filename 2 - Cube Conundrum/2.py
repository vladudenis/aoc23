# Cube Conundrum

"""
PART 1
Problem:
As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue.
Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to
figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag,
grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its
ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were
revealed from the bag (like 3 red, 5 green, 4 blue).

The Elf would first like to know which games would have been possible if the bag contained only
12 red cubes, 13 green cubes, and 14 blue cubes?

Goal:
Determine which games would have been possible if the bag had been loaded with only
12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
"""
import re


def is_game_possible(game: str, config: [str]):
    outcomes = game.split(",")

    for c in config:
        c_nr = int(c.split(" ")[0])
        c_color = c.split(" ")[1]

        for o in outcomes:
            o = o.strip()
            o_nr = int(o.split(" ")[0])
            o_color = o.split(" ")[1]

            if o_color == c_color and o_nr > c_nr:
                return False

    return True


def count_possible_game_ids(config: [str]):
    id_count = 0

    with open("2_input.txt", "r") as f:
        games = f.readlines()

        for g in games:
            g_id = re.match("(?:(?!:).)*", g).group().split(" ")[1]
            g_info = re.search("(?<=:).*", g).group().replace(";", ",")

            if is_game_possible(g_info, config):
                id_count += int(g_id)

    return id_count


configuration = ["12 red", "13 green", "14 blue"]
print(count_possible_game_ids(configuration))
# Answer: 2105

"""
PART 2
Problem:
As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of 
cubes of each color that could have been in the bag to make the game possible?

The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.

Goal:
For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""


def determine_min_cubes(game: str):
    outcomes = game.split(",")
    r_min, g_min, b_min = None, None, None

    for o in outcomes:
        o = o.strip()
        o_nr = int(o.split(" ")[0])
        o_color = o.split(" ")[1]

        if o_color == "red" and (r_min is None or r_min < o_nr):
            r_min = o_nr
        elif o_color == "green" and (g_min is None or g_min < o_nr):
            g_min = o_nr
        elif o_color == "blue" and (b_min is None or b_min < o_nr):
            b_min = o_nr

    return r_min, g_min, b_min


def count_power_of_min_cubes():
    power_count = 0

    with open("2_input.txt", "r") as f:
        games = f.readlines()

        for g in games:
            g_info = re.search("(?<=:).*", g).group().replace(";", ",")
            r_min, g_min, b_min = determine_min_cubes(g_info)
            power_count += r_min * g_min * b_min

    return power_count


print(count_power_of_min_cubes())
# Answer: 72422
