from collections import defaultdict
from types import new_class

from adventofcode2021.input_data import day06 as raw_data

data = [int(x) for x in raw_data.split(",")]


def build_state(ages: list):
    state = defaultdict(int)
    for a in ages:
        state[a] += 1
    return state


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
    state = build_state(data)
    for _ in range(number_of_iterations):
        state = create_new_state(state)
    print(sum_numbers_fish(state))


if __name__ == "__main__":
    simulate_growth(80)
    simulate_growth(256)
