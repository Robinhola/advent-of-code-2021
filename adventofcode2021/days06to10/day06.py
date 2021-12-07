from collections import defaultdict, Counter
from types import new_class

from adventofcode2021.input_data import day06 as raw_data

data = [int(x) for x in raw_data.split(",")]


def create_new_state(state: dict):
    new_state = defaultdict(int)
    for a, n in state.items():
        if a == 0:
            new_state[6] += n  # reset each fish
            new_state[8] += n  # spawn new fish
        else:
            new_state[a - 1] += n  # update fish
    return new_state


def sum_numbers_fish(state: dict):
    return sum(state.values())


def simulate_growth(number_of_iterations: int):
    fish = Counter(data)
    for _ in range(number_of_iterations):
        fish = create_new_state(fish)
    print(sum_numbers_fish(fish))


if __name__ == "__main__":
    simulate_growth(80)
    simulate_growth(256)
