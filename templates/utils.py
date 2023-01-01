
import numpy as np


class SudokuException(Exception):
    """Raised on invalid sudoku board"""

    def __init__(self, message: str) -> None:
        self.message = message

class Board:
    def __init__(self, data: np.ndarray) -> None:
        if not data.shape == (9, 9):
            raise AttributeError(f"Bad input shape: {data.shape} must be (9, 9)")
        self.data: np.ndarray = data.astype(np.int8)
        if not self.validate_board():
            raise SudokuException("Sudoku board is not valid")

        self.empty: list[tuple[int, int]] = []
        self.empty.append((-10, -10))
        for i in range(len(self.data)-1, -1, -1):
            for j in range(len(self.data[0])-1, -1, -1):
                if self.data[i, j] == 0:
                    self.empty.append((i, j))

    def validate_position(self, i: int, j: int, num: int) -> bool:

        # validate row
        for k in range(len(self.data[0])):
            if k == j:
                continue
            if num == self.data[i, k]:
                return False 

        # validate column
        for k in range(len(self.data)):
            if k == i:
                continue

            if num == self.data[k, j]:
                return False

        # validate box
        i_cell = i // 3
        j_cell = j // 3

        for k in range(i_cell*3, i_cell*3 + 3):
            for l in range(j_cell*3, j_cell*3 + 3):
                if k == i and l == j:
                    continue

                if num == self.data[k, l]:
                    return False

        return True

    def validate_board(self) -> bool:
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                num = self.data[i, j]
                if num == 0:
                    continue
                if not self.validate_position(i, j, num):
                    return False

        return True

    def solve(self):
        current = {}
        solved_id = []
        for i, j in self.empty:
            current[f"{i}{j}"] = 1

        i, j = self.empty.pop()
        while len(self.empty) > 0:
            solving = current[f"{i}{j}"]
            if solving == 10:
                current[f"{i}{j}"] = 1
                self.empty.append((i, j))
                self.data[i, j] = 0
                i, j = solved_id.pop()
                current[f"{i}{j}"] += 1
                continue

            if self.validate_position(i, j, solving):
                self.data[i, j] = solving
                solved_id.append((i, j))
                i, j = self.empty.pop()
            else:
                current[f"{i}{j}"] += 1

        return self.data

    def solve2(self):
        """Backtracking algorithm"""
        solved_id = []

        i, j = self.empty.pop()
        while len(self.empty) > 0:
            solving = self.data[i, j] + 1
            if solving == 10:
                self.data[i, j] = 0
                self.empty.append((i, j))
                try:
                    i, j = solved_id.pop()
                except IndexError:
                    raise SudokuException("This sudoku does not have solution")
                continue

            if self.validate_position(i, j, solving):
                self.data[i, j] = solving
                solved_id.append((i, j))
                i, j = self.empty.pop()
            else:
                self.data[i, j] += 1

        return self.data
                
# board = np.array([
#     [5, 8, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 2, 0, 9, 0, 8, 1],
#     [0, 0, 0, 0, 0, 1, 5, 0, 3],
#     [1, 0, 7, 0, 0, 0, 9, 3, 0],
#     [0, 0, 0, 0, 8, 0, 0, 0, 0],
#     [0, 3, 8, 0, 0, 0, 2, 0, 4],
#     [4, 0, 6, 9, 0, 0, 0, 0, 0],
#     [9, 1, 0, 5, 0, 6, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 2, 9]
# ])

board = np.array([
    [2, 0, 0, 8, 3, 0, 7, 0, 0],
    [7, 0, 4, 0, 0, 2, 3, 5, 0],
    [0, 0, 8, 0, 0, 0, 0, 0, 0],
    [0, 5, 2, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 9, 0, 4, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 8, 2, 0],
    [0, 0, 0, 0, 0, 0, 9, 0, 0],
    [0, 7, 6, 4, 0, 0, 1, 0, 2],
    [0, 0, 3, 0, 6, 9, 0, 0, 7]
])

if __name__ == "__main__":
    b = Board(board)
    out = b.solve2()
    print(out)