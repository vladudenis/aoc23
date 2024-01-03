# If You Give A Seed A Fertilizer

"""
PART 1
Problem:
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into
numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert
a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil
to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire
ranges of numbers that can be converted. Each line within a map contains three numbers:
the destination range start, the source range start, and the range length.

Ex.: 50 98 2
The first line has a destination range start of 50, a source range start of 98, and a range length of 2.
This line means that the source range starts at 98 and contains two values: 98 and 99.
The destination range is the same length, but it starts at 50, so its two values are 50 and 51.
With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds
to soil number 51.

Any source numbers that aren't mapped correspond to the same destination number!

Goal:
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that
needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this
you'll need to convert each seed number through other categories until you can find its corresponding location number.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""


class Mapping:
    def __init__(self, name: str):
        self.name = name

        name_split = name.split("-")
        self.source_name = name_split[0]
        self.destination_name = name_split[2]

        self.map = []

    def add_mapping(self, source_range_start: int, destination_range_start: int, range_length: int):
        source_range_end = source_range_start + range_length - 1
        destination_range_end = destination_range_start + range_length - 1

        self.map.append((source_range_start, source_range_end, destination_range_start, destination_range_end))


def parse_input():
    with open("5_input.txt") as f:
        almanac = f.readlines()
        seeds = []
        mappings = []

        for idx, line in enumerate(almanac):
            if len(line) > 1:
                line_split = line.split(" ")

                if idx == 0:
                    for seed in line_split[1:]:
                        seeds.append(int(seed))
                elif len(line_split) == 2:
                    new_map = Mapping(line_split[0])
                    mappings.append(new_map)
                else:
                    source_start = int(line_split[1])
                    dest_start = int(line_split[0])
                    range_len = int(line_split[2])

                    mappings[-1].add_mapping(source_start, dest_start, range_len)

    return seeds, mappings


def find_min_location(seeds: [int], mappings: []):
    sources = seeds

    for mapping in mappings:
        next_sources = []

        for source in sources:
            for src_s, src_e, dest_s, dest_e in mapping.map:
                if src_s <= source <= src_e:
                    offset = source - src_s
                    destination = dest_s + offset

            next_sources.append(destination)

        sources = next_sources

    return min(sources)


s, m = parse_input()
minimum = find_min_location(s, m)

print(minimum)
# Answer: 486613012

"""
PART 2
Problem:
Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers. The values on the 
initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is 
the length of the range.

Goal:
Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest 
location number that corresponds to any of the initial seed numbers?
"""
import numpy as np

def parse_input_with_seed_ranges():
    with open("5_input.txt") as f:
        almanac = f.readlines()
        seed_ranges = []
        mappings = []

        for idx, line in enumerate(almanac):
            if len(line) > 1:
                line_split = line.split(" ")

                if idx == 0:
                    seed_nums = []

                    for seed in line_split[1:]:
                        seed_nums.append(int(seed))

                    for i in range(0, len(seed_nums), 2):
                        range_start = seed_nums[i]
                        range_end = range_start + seed_nums[i + 1] - 1
                        seed_ranges.append((range_start, range_end))

                elif len(line_split) == 2:
                    new_map = Mapping(line_split[0])
                    mappings.append(new_map)
                else:
                    source_start = int(line_split[1])
                    dest_start = int(line_split[0])
                    range_len = int(line_split[2])

                    mappings[-1].add_mapping(source_start, dest_start, range_len)

    return seed_ranges, mappings


s_range, m = parse_input_with_seed_ranges()
m.reverse()


def resolve_reverse_map(mapping, index):
    for src_s, src_e, dest_s, dest_e in mapping:
        if dest_s <= index <= dest_e:
            return index - dest_s + src_s

    return index


def find_min_location_brute_force(start: int, end: int, step: int):
    for i in range(start, end, step):
        seed = i

        for mapping in m:
            seed = resolve_reverse_map(mapping.map, seed)

        for start_range, end_range in np.array(s_range):
            if start_range <= seed <= end_range:
                return i
        else:
            continue


first_iteration = find_min_location_brute_force(0, 100000000, 1000)
second_iteration = find_min_location_brute_force(first_iteration - 1000, first_iteration + 1, 1)

print(second_iteration)
# Answer: 56931769
