from typing import Annotated, Set, Tuple

from pydantic import BaseModel, Field


class Square(BaseModel):
    possibles: Annotated[Set[int], 9] = Field({1, 2, 3, 4, 5, 6, 7, 8, 9})


class Game(BaseModel):
    rows: Annotated[Tuple[Square], 9]


def main():
    print("Under construction")
