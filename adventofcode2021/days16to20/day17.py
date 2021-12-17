from dataclasses import dataclass

raw_data = """target area: x=192..251, y=-89..-59"""
raw_data = """target area: x=20..30, y=-10..-5"""
target_area = ((20, 30), (-10, -5))
target_area = ((192, 251), (-89, -59))
(x1, x2), (y1, y2) = target_area


def apply_drag(value):
    if value > 0:
        return value - 1
    elif value < 0:
        return value + 1
    return 0


@dataclass
class Probe:
    position: tuple
    velocity: tuple
    highest_y: int = 0

    def step(self):
        x, y = self.position
        dx, dy = self.velocity

        x += dx
        y += dy

        dx = apply_drag(dx)
        dy -= 1

        self.highest_y = max(y, self.highest_y)

        self.position = (x, y)
        self.velocity = (dx, dy)

    def can_reach_x(self):
        x, _ = self.position
        dx, _ = self.velocity
        return (x1 <= x <= x2) or (x < x1 and dx > 0) or (x > x2 and dx < 0)

    def can_reach_y(self):
        _, y = self.position
        _, dy = self.velocity
        return (y1 <= y <= y2) or (y < y1 and dy > 0) or (y > y2)

    def has_reach(self):
        x, y = self.position
        return x1 <= x <= x2 and y1 <= y <= y2

    def after_any_step(self):
        while self.can_reach_x() and self.can_reach_y():
            if self.has_reach():
                return True
            self.step()
        return False


def validate_probe(intial_velocity):
    probe = Probe((0, 0), intial_velocity)
    return probe.after_any_step(), probe


def sum_until(n):
    return n * (n + 1) / 2


def find_best_x():
    n = 1
    while sum_until(n) < x1:
        n += 1
    return n


def find_last_x():
    n = 1
    while sum_until(n) <= x2:
        n += 1
    return n  # not included


def find_first_y(start):
    x = find_best_x()
    y = start
    reached = False
    while not reached:
        y += 1
        velocity = (x, y)
        reached, probe = validate_probe(velocity)
    return y


def part1():
    for v in ((7, 2), (6, 3), (9, 0), (17, -4), (6, 9), (20, 88), (20, 89)):
        reached, probe = validate_probe(v)
        print(reached, probe.highest_y)

    # Manual work
    _, probe = validate_probe((20, 88))
    return probe.highest_y


def part2():
    first_x, last_x = 0, 300
    first_y, last_y = -100, 90

    count = 0
    for x in range(first_x, last_x):
        for y in range(first_y, last_y):
            v = (x, y)
            reached, probe = validate_probe(v)
            if reached:
                count += 1
    return count

    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
