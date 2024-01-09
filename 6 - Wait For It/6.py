# Wait for It

"""
PART 1
Problem:
As part of signing up, you get a sheet of paper (your puzzle input) that lists the time allowed for each race and also
the best distance ever recorded in that race. To guarantee you win the grand prize, you need to make sure you go
farther in each race than the current record holder.

The organizer brings you over to the area where the boat races are held. The boats are much smaller than you expected -
they're actually toy boats, each with a big button on top. Holding down the button charges the boat, and releasing the
button allows the boat to move. Boats move faster if their button was held longer, but time spent holding the button
counts against the total race time. You can only hold the button at the start of the race, and boats don't move
until the button is released.

Your toy boat has a starting speed of zero millimeters per millisecond.
For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases
by one millimeter per millisecond.

Goal:
Determine the number of ways you could beat the record in each race.
What do you get if you multiply these numbers together?
"""
import math

with open("6_input.txt", "r") as f:
    lines = f.readlines()
    times = []
    distances = []

    for line in lines:
        if "Time" in line:
            times_list = line[len("Time") + 1:].strip().split(" ")

            for entry in times_list:
                if entry.isnumeric():
                    times.append(entry)
        elif "Distance" in line:
            distances_list = line[len("Distance") + 1:].strip().split(" ")

            for entry in distances_list:
                if entry.isnumeric():
                    distances.append(entry)
win_product = 1

for idx, time in enumerate(times):
    time = int(time)
    ways_to_win = 0

    for time_pressing in range(time):
        if (time - time_pressing) * time_pressing > int(distances[idx]):
            ways_to_win += 1

    win_product *= ways_to_win

print(win_product)

"""
PART 2
Problem:
As the race is about to start, you realize the piece of paper with race times and record distances you got earlier
actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

Goal: How many ways can you beat the record in this one much longer race?
"""


def quadratic(time, record):
    x1 = ((time - math.sqrt(time*time - 4 * record)) / 2)
    x0 = ((time + math.sqrt(time*time - 4 * record)) / 2)
    if int(x1) == x1:
        x1 += 1
    if int(x0) == x0:
        x0 -= 1
    return math.floor(x0) - math.ceil(x1) + 1


with open("6_input.txt", "r") as f:
    lines = f.readlines()
    time = ""
    distance = ""

    for line in lines:
        if "Time" in line:
            times_list = line[len("Time") + 1:].strip().split(" ")

            for entry in times_list:
                if entry.isnumeric():
                    time += entry
        elif "Distance" in line:
            distances_list = line[len("Distance") + 1:].strip().split(" ")

            for entry in distances_list:
                if entry.isnumeric():
                    distance += entry

time = int(time)
distance = int(distance)
print(quadratic(time, distance))
