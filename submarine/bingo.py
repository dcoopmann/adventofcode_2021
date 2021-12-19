from pprint import pprint

import pytest

puzzle_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


@pytest.mark.parametrize("b_no, b_row, b_col, exp_no",[(0,0,0,22),(0,0,1,13),(0,0,2,17),(0,0,3,11),(0,0,4,0),(1,3,0,20),(2,4,4,7)])
def test_cut_boards(b_no, b_row, b_col, exp_no):
    bs = BingoSubsystem(puzzle_input)

    assert bs.raw_boards[b_no][b_row][b_col] == str(exp_no)

class BingoSubsystem:
    def __init__(self, input) -> None:
        self.raw_input = input
        self.raw_boards = []

        self._prepare_input()
        self._cut_boards()

    def _prepare_input(self):    
        numbers_board = self.raw_input.split()
        self.numbers_draw = numbers_board.pop(0)
        self.board_number_stream = numbers_board

    def _cut_boards(self):
        while len(self.board_number_stream) != 0:
            br = []
            for i in range(0,5):
                bc = []
                for x in range(0,5):
                    bc.append(self.board_number_stream.pop(0))

                br.append(bc)

            self.raw_boards.append(br)

class BingoBoard:

    def __init__(self) -> None:
        self.layout = []
        self.marked_layout = []
    
    def _load_board(self):
        pass


if __name__ == "__main__":
    

    bs = BingoSubsystem(puzzle_input)
    pprint(bs.raw_input)
    pprint(bs.raw_boards)
