from typing import Annotated, Set, Tuple

from pydantic import BaseModel, Field

SIZE = 4


class Coord(BaseModel):
    x: int
    y: int


class Square(BaseModel):
    possibles: Set[int] = Field(set(range(1, SIZE + 1)))


class Game(BaseModel):
    rows: Annotated[Tuple[Annotated[Tuple[Square], SIZE]], SIZE] = Field(
            tuple(tuple(Square() for _ in range(SIZE)) for _ in range(SIZE)))
    columns: Annotated[Tuple[Annotated[Tuple[Square], SIZE]], SIZE] = Field(
            tuple(tuple(Square() for _ in range(SIZE)) for _ in range(SIZE)))
    boxes: Annotated[Tuple[Annotated[Tuple[Square], SIZE]], SIZE] = Field(
            tuple(tuple(Square() for _ in range(SIZE)) for _ in range(SIZE)))


def main():
    print("Under construction")
    print(f"{Game()}")
