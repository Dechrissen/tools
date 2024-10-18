# This scripts contains some functions to create a csv file containing the difference between Gen 1 and Gen 2 learnsets
# (level-up, TMs, tutor moves, egg moves)

import pokebase as pb
import csv
import time
from gen1_moves_and_machines import *


# mon = pb.pokemon(user_input)
user_input_lower = int(input("Enter starting Pokedex number: "))
user_input_upper = int(input("Enter ending Pokedex number: "))

# game = 'red-blue'
# game = 'yellow'
# game = 'gold-silver'
# game = 'crystal'

# learn_method = 'level-up'
# learn_method = 'machine'
# learn_method = 'tutor'


def getLearnset(game, pokemon, method) -> list:
    moves = pokemon.moves
    learnset = []
    for move in moves:
        for vg in move.version_group_details:
            learn_method = str(vg.move_learn_method)
            version = str(vg.version_group)
            if version == game and learn_method == method:
                learnset.append(move.move.name)

    return learnset


# if pokemon learns new moves via TM in gen 2, and that TM is a TM in gen 1, print it in a list
def getLearnsetDiffBetween2(pokemon, method, includeGen2TMs=False) -> list:
    gen_1_learnset = getLearnset("yellow", pokemon, method)
    gen_2_learnset = getLearnset("crystal", pokemon, method)

    diff = []

    if method == "machine" and includeGen2TMs == True:
        for move in gen_2_learnset:
            if (move not in gen_1_learnset) and (move in gen1moves):
                diff.append(move)
        diff = [move for move in diff if move not in gen1tms]
    elif method == "machine":
        for move in gen_2_learnset:
            if (move not in gen_1_learnset) and (move in gen1tms):
                diff.append(move)
    elif method == "level-up":
        for move in gen_2_learnset:
            if (move not in gen_1_learnset) and (move in gen1moves):
                diff.append(move)
    else:
        print("unknown method")
        return

    return diff


def getTutorMoves(pokemon) -> list:
    new_tutor_moves = []
    gen_1_levelup_learnset = getLearnset("yellow", pokemon, "level-up")
    gen_1_tm_learnset = getLearnset("yellow", pokemon, "machine")
    tutor_moves = getLearnset("crystal", pokemon, "tutor")

    for move in tutor_moves:
        if (move in gen_1_levelup_learnset) and (move in gen_1_tm_learnset):
            pass
        elif move in gen_1_tm_learnset:
            pass
        elif move not in gen_1_tm_learnset:
            new_tutor_moves.append(move)

    return new_tutor_moves


def getEggMoves(pokemon) -> list:
    egg_moves = getLearnset("crystal", pokemon, "egg")
    egg_moves = [move for move in egg_moves if move in gen1moves]
    return egg_moves


def createDataForCsv(lower, upper, data_rows):
    for i in range(lower, upper + 1):
        mon = pb.pokemon(i)
        row = [
            mon.species.name,
            getLearnsetDiffBetween2(mon, "level-up"),
            getLearnsetDiffBetween2(mon, "machine"),
            getLearnsetDiffBetween2(mon, "machine", True),
            getTutorMoves(mon),
            getEggMoves(mon),
        ]
        data_rows.append(row)
        print("learnset data created for", mon.species.name)
        time.sleep(2)
    return data_rows


###########################################################################################

# create initial data array for csv
starter_data = [
    [
        "Pokemon",
        "Level-up moves to add to Gen 1 learnset",
        "TMs to add to Gen 1 learnset (if TM exists in Gen 1)",
        "New TMs to add to Gen 1 learnset (if TM does not exist in Gen 1)",
        "Tutor moves to add TM support for",
        "Egg moves from Gen 2",
    ]
]

data = createDataForCsv(user_input_lower, user_input_upper, starter_data)

# File path for the CSV file
csv_file_path = "datadummy.csv"

# Open the file in write mode
with open(csv_file_path, mode="w", newline="") as file:
    # Create a csv.writer object
    writer = csv.writer(file)
    # Write data to the CSV file
    writer.writerows(data)

print("done")
print("csv created:", csv_file_path)


# small script to get list of gen 1 tms
# game = 'red-blue'
# gen1tms = []
# Get a list of EVERY move from the API.
# for m in range (1,166):
#     move = pb.move(m)
#     if str(move.generation.name) == 'generation-i':
#         #proceed
#         # if len(move.machines) >= 1:
#         #     for item in move.machines:
#         #         if str(item.version_group.name) == game:
#         #             gen1tms.append(move.name)
#         #             break
#         gen1tms.append(move.name)
#         print('wrote', move.name)
