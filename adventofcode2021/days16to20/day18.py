from dataclasses import dataclass
from os import defpath
import re
from types import new_class
from typing import Optional, Union
import math

raw_data = """replace_me"""


@dataclass
class SnailFishNumber:
    left: Optional["SnailFishNumber"]
    right: Optional["SnailFishNumber"]
    depth: int
    parent: Optional["SnailFishNumber"] = None
    value: Optional[int] = None

    @classmethod
    def addition(cls, a, b):
        a.increase_depth()
        b.increase_depth()
        sum = cls(a, b, 0)

        to_explode, to_split = sum.look_for_node(4)
        print("after addition", end="")
        while to_explode is not None or to_split is not None:
            print(sum)
            if to_explode:
                print("after explode", end="")
                cls.explode_node(to_explode)
            if to_split:
                print("after split", end="")
                cls.split_node(to_split)
            to_explode, to_split = sum.look_for_node(4)

        print(sum)
        return sum

    @classmethod
    def explode_node(cls, node: "SnailFishNumber"):
        if node.find_left() is not None:
            node.find_left().value += node.left.value
        if node.find_right() is not None:
            node.find_right().value += node.right.value
        if node.parent.left == node:
            node.parent.left = cls(None, None, node.depth, node.parent, 0)
        elif node.parent.right == node:
            node.parent.right = cls(None, None, node.depth, node.parent, 0)

    @classmethod
    def split_node(cls, node: "SnailFishNumber"):
        value = node.value
        node.left = cls(None, None, node.depth + 1, node, math.floor(value / 2.0))
        node.right = cls(None, None, node.depth + 1, node, math.ceil(value / 2.0))
        node.value = None

    def look_for_node(self, depth):
        if self.value and self.value > 9:
            return None, self

        if self.value is None and self.depth == depth:
            return self, None

        if self.left:
            a, b = self.left.look_for_node(depth)
            if a is not None or b is not None:
                return a, b

        if self.right:
            a, b = self.right.look_for_node(depth)
            if a is not None or b is not None:
                return a, b

        return None, None

    def increase_depth(self):
        self.depth += 1
        for x in (self.left, self.right):
            if x.value is None:
                x.increase_depth()

    @classmethod
    def from_input(cls, string, depth=0, parent=None):
        middle, opened = None, 0
        for i, c in enumerate(string):
            if c == "[":
                opened += 1
            elif c == "]":
                opened -= 1
            elif c == "," and opened == 1:
                middle = i
                break

        if middle is None:
            return cls(None, None, depth, parent, int(string))

        new_node = cls(None, None, depth, parent)

        new_node.left = cls.from_input(string[1:middle], depth + 1, new_node)
        new_node.right = cls.from_input(
            string[middle + 1 : len(string) - 1], depth + 1, new_node
        )

        return new_node

    def find_left(self):
        if not self.parent:
            return None
        if self.parent.left == self:
            return self.parent.find_left()
        else:
            return self.parent.left

    def find_right(self):
        if not self.parent:
            return None
        if self.parent.right == self:
            return self.parent.find_right()
        else:
            return self.parent.right

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        # return f"[{str(self.left)},{str(self.right)}]({self.depth})"
        return f"[{str(self.left)},{str(self.right)}]"

    def __add__(self, other):
        return SnailFishNumber.addition(self, other)


def part1():
    a = SnailFishNumber.from_input("[1,1]")
    b = SnailFishNumber.from_input("[2,2]")
    d = SnailFishNumber.from_input("[3,3]")
    c = SnailFishNumber.from_input("[[[[[9,8],1],2],3],4]")

    e = SnailFishNumber.from_input("[[[[4,3],4],4],[7,[[8,4],9]]]")
    f = SnailFishNumber.from_input("[1,1]")
    # return e
    return e + f


def part2():
    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
