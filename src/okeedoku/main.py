from typing import Annotated, Set, Tuple, Generator
from random import choice
from numpy import ndindex

from pydantic import BaseModel, Field

BOX_SIDE_LENGTH = 3
SIZE = BOX_SIDE_LENGTH ** 2


class Coord(BaseModel):
    row: int
    column: int

    @property
    def box(self) -> int:
        return (
            self.row // BOX_SIDE_LENGTH
        ) * BOX_SIDE_LENGTH + self.column // BOX_SIDE_LENGTH

    def __hash__(self) -> int:
        return hash(f"{self.row}_{self.column}")


class Square(BaseModel):
    possibles: Set[int] = Field(set(range(1, SIZE + 1)))


class Game(BaseModel):
    squares: Annotated[Tuple[Annotated[Tuple[Square], SIZE]], SIZE] = Field(
        tuple(tuple(Square() for _ in range(SIZE)) for _ in range(SIZE))
    )
    new_knowns: Set[Coord] = Field(default_factory=set)
    knowns: Set[Coord] = Field(default_factory=set)

    def set_square_val(self, coord: Coord, val: int) -> None:
        if val < 1 or val > SIZE:
            raise ValueError

        self.squares[coord.row][coord.column].possibles = set({val})
        self.process_possibles(coord, val)

    def process_possibles(self, coord, val) -> None:
        for bcoord in [Coord(row=coord.row, column=i) for i in range(SIZE)]:
            self.discard_possibles(coord, bcoord, val)

        for bcoord in [Coord(row=i, column=coord.column) for i in range(SIZE)]:
            self.discard_possibles(coord, bcoord, val)

        for bcoord in enumerate_box(coord.box):
            self.discard_possibles(coord, bcoord, val)

    def discard_possibles(self, known, bcoord, val) -> None:
        if bcoord == known:
            return
        self.squares[bcoord.row][bcoord.column].possibles.discard(val)
        if (
            len(self.squares[bcoord.row][bcoord.column].possibles) == 1
            and bcoord not in self.knowns
        ):
            self.new_knowns.add(bcoord)

    def process_new_knowns(self) -> None:
        while len(self.new_knowns) > 0:
            coord = self.new_knowns.pop()
            self.knowns.add(coord)
            self.process_possibles(
                coord, list(self.squares[coord.row][coord.column].possibles)[0]
            )

    def get_square(self, coord: Coord) -> Square:
        return self.squares[coord.row][coord.column]

    def rand_fill(self) -> None:
        unknowns = [Coord(row=x, column=y) for x, y in ndindex((SIZE, SIZE))]
        pick = choice([u for u in unknowns if u not in self.knowns])
        sq = self.get_square(pick)
        print(f"{pick}, {sq}")
        self.set_square_val(pick, choice(list(sq.possibles)))
        self.process_new_knowns()
        print(self)

    def __str__(self) -> str:
        ret = ""
        for x in range(SIZE):
            for y in range(SIZE):
                square = self.squares[x][y]
                if len(square.possibles) == SIZE:
                    ret += "{ALL}"
                elif len(square.possibles) > 1:
                    ret += str(square.possibles)
                elif len(square.possibles) == 1:
                    ret += str(list(square.possibles)[0])
                else:
                    ret += "X"
            ret += "\n"
        return ret


def enumerate_box(box_no: int) -> Generator[Coord, None, None]:
    if box_no >= SIZE or box_no < 0:
        raise ValueError

    box_coord = Coord(
        row=(box_no) // BOX_SIDE_LENGTH, column=(box_no) % BOX_SIDE_LENGTH
    )
    print(f"enumerating box {box_no} coord {box_coord}")
    for x in range(BOX_SIDE_LENGTH):
        for y in range(BOX_SIDE_LENGTH):
            coord = Coord(
                row=x + (box_coord.row * BOX_SIDE_LENGTH),
                column=y + (box_coord.column * BOX_SIDE_LENGTH),
            )
            print(coord)
            yield coord


def main():
    print("Under construction")
    print(f"{Game()}")
