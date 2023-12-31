# Scratchcards

"""
PART 1
Problem:
The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their opaque
covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by a
vertical bar (|): a list of winning numbers and then a list of numbers you have.
You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list
of winning numbers. The first match makes the card worth one point and each match after the first doubles
the point value of that card.

Goal: Take a seat in the large pile of colorful cards. How many points are they worth in total?
"""


def parse_line(l: str):
    entries = l.split(" ")
    searching_nums = False
    c = []
    w = []

    for i, entry in enumerate(entries):
        if i == 0 or i == 1:
            continue
        elif searching_nums:
            if entry.isnumeric():
                w.append(int(entry))
            elif "\n" in entry:
                w.append(int(entry[:3]))
        else:
            if entry == "|":
                searching_nums = True
            elif entry.isnumeric():
                c.append(int(entry))

    return c, w


def get_points_sum(c: [int], w: [int]):
    p = 0

    for i in c:
        if i in w:
            if p == 0:
                p += 1
            else:
                p = p * 2

    return p


with open("4_input.txt", "r") as f:
    lines = f.readlines()
    winning_nums = []

    for line in lines:
        card_nums, nums = parse_line(line)
        points_sum = get_points_sum(card_nums, nums)

        winning_nums.append(points_sum)

    print(sum(winning_nums))
    # Answer: 20667

"""
PART 2
Problem:
There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to
the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. 
So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. 
So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the 
original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to
win any more cards. (Cards will never make you copy a card past the end of the table.)

Goal:
Process all of the original and copied scratchcards until no more scratchcards are won. 
Including the original set of scratchcards, how many total scratchcards do you end up with?
"""

# Note: Starting from Card 1 all the way to Card n, we see that the number of instances of Card i is [1, i].


def get_matches(c: [int], w: [int]):
    m = 0

    for i in c:
        if i in w:
            m += 1

    return m


with open("4_input.txt", "r") as f:
    lines = f.readlines()
    instances = [1 for _ in range(len(lines))]

    for idx, line in enumerate(lines):
        card_nums, nums = parse_line(line)
        matches = get_matches(card_nums, nums)

        for j in range(matches):
            instances[idx + matches - j] += instances[idx]

    print(sum(instances))
    # Answer: 5833065
