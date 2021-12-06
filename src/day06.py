from collections import defaultdict
from types import new_class


raw_data = """1,3,1,5,5,1,1,1,5,1,1,1,3,1,1,4,3,1,1,2,2,4,2,1,3,3,2,4,4,4,1,3,1,1,4,3,1,5,5,1,1,3,4,2,1,5,3,4,5,5,2,5,5,1,5,5,2,1,5,1,1,2,1,1,1,4,4,1,3,3,1,5,4,4,3,4,3,3,1,1,3,4,1,5,5,2,5,2,2,4,1,2,5,2,1,2,5,4,1,1,1,1,1,4,1,1,3,1,5,2,5,1,3,1,5,3,3,2,2,1,5,1,1,1,2,1,1,2,1,1,2,1,5,3,5,2,5,2,2,2,1,1,1,5,5,2,2,1,1,3,4,1,1,3,1,3,5,1,4,1,4,1,3,1,4,1,1,1,1,2,1,4,5,4,5,5,2,1,3,1,4,2,5,1,1,3,5,2,1,2,2,5,1,2,2,4,5,2,1,1,1,1,2,2,3,1,5,5,5,3,2,4,2,4,1,5,3,1,4,4,2,4,2,2,4,4,4,4,1,3,4,3,2,1,3,5,3,1,5,5,4,1,5,1,2,4,2,5,4,1,3,3,1,4,1,3,3,3,1,3,1,1,1,1,4,1,2,3,1,3,3,5,2,3,1,1,1,5,5,4,1,2,3,1,3,1,1,4,1,3,2,2,1,1,1,3,4,3,1,3"""

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
