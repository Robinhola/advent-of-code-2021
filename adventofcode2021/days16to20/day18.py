from dataclasses import dataclass
from os import defpath
import re
from types import new_class
from typing import Optional, Union
import math

raw_data = """[1,1]
[2,2]
[3,3]
[4,4]"""

raw_data = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""

# raw_data = """[[[[4,3],4],4],[7,[[8,4],9]]]
# [1,1]"""

raw_data = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""

raw_data = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""


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
        a.parent = sum
        b.parent = sum

        to_explode, to_split = sum.look_for_node(4)
        while to_explode is not None or to_split is not None:
            if to_explode:
                cls.explode_node(to_explode)
            if to_split:
                cls.split_node(to_split)
            to_explode, to_split = sum.look_for_node(4)

        return sum

    @classmethod
    def explode_node(cls, node: "SnailFishNumber"):
        if node.find_left() is not None:
            node.find_left().value += node.left.value
        if node.find_right() is not None:
            node.find_right().value += node.right.value

        if node.parent.left is node:
            node.parent.left = cls(None, None, node.depth, node.parent, 0)
        elif node.parent.right is node:
            node.parent.right = cls(None, None, node.depth, node.parent, 0)

    @classmethod
    def split_node(cls, node: "SnailFishNumber"):
        value = node.value
        depth = node.depth
        node.left = cls(None, None, depth + 2, node, math.floor(value / 2.0))
        node.right = cls(None, None, depth + 2, node, math.ceil(value / 2.0))
        node.value = None
        node.depth = depth + 1

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

    def right_most(self):
        if self.value is not None:
            return self
        else:
            return self.right.right_most()

    def left_most(self):
        if self.value is not None:
            return self
        else:
            return self.left.left_most()

    def find_left(self):
        if not self.parent:
            return None
        if self.parent.left is self:
            return self.parent.find_left()
        return self.parent.left.right_most()

    def find_right(self):
        if not self.parent:
            return None
        if self.parent.right is self:
            return self.parent.find_right()
        return self.parent.right.left_most()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        # return f"[{str(self.left)},{str(self.right)}]({self.depth})"
        return f"[{str(self.left)},{str(self.right)}]"

    def __add__(self, other):
        return SnailFishNumber.addition(self, other)


def part1():
    number = None
    for l in raw_data.splitlines():
        if number == None:
            number = SnailFishNumber.from_input(l)
        else:
            number = number + SnailFishNumber.from_input(l)
        print(number)
    return number


def part2():
    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
