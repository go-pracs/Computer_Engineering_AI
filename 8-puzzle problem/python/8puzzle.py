from functools import cmp_to_key


class Board:
    def __init__(self, currentBoard, blankTileIndex_row, blankTileIndex_col, blankTileStatus):
        self.currentBoard = currentBoard
        self.blankTileIndex_row = blankTileIndex_row
        self.blankTileIndex_col = blankTileIndex_col
        self.blankTileStatus = blankTileStatus
        self.misplacedTilesCount = 0
        self.manhattan_distance = 0
        self.parent_state = None

    def is_goal(self):
        return self.currentBoard == goal_board

    def swapTiles(self, oldBlankTilePosition_row, oldBlankTilePosition_col):
        self.currentBoard[self.blankTileIndex_row][self.blankTileIndex_col], \
        self.currentBoard[oldBlankTilePosition_row][oldBlankTilePosition_col] = \
            self.currentBoard[oldBlankTilePosition_row][oldBlankTilePosition_col], \
            self.currentBoard[self.blankTileIndex_row][self.blankTileIndex_col]

    def setMisplacedTilesCount(self):
        count = 0
        for row in range(3):
            for col in range(3):
                if self.currentBoard[row][col] != 0 and self.currentBoard[row][col] != goal_board[row][col]:
                    count += 1

        self.misplacedTilesCount = count

    def set_manhattan_distance(self):
        summ = 0
        for i in range(3):
            for j in range(3):
                target = goal_board[i][j]
                for row in range(3):
                    flag = False
                    for col in range(3):
                        if self.currentBoard[row][col] == target:
                            summ += abs(i-row) + abs(j-col)
                            flag = True
                            break
                    if flag:
                        break
        self.manhattan_distance = summ


def isValid(row, col):
        return 0 <= row <= 2 and 0 <= col <= 2


def copy_board(current_board):
    return [[current_board[row][col] for col in range(3)] for row in range(3)]



def get_successors(current_state):
    successors = []
    mapp = {(-1, 0) : 'UP', (1, 0) : 'DOWN', (0, -1) : 'LEFT', (0, 1) : 'RIGHT'}
    generators = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    for generator in generators:

        newBlankTilePosition_row = current_state.blankTileIndex_row + generator[0]
        newBlankTilePosition_col = current_state.blankTileIndex_col + generator[1]

        if isValid(newBlankTilePosition_row, newBlankTilePosition_col):
            new_board = Board(copy_board(current_state.currentBoard), newBlankTilePosition_row, newBlankTilePosition_col, "Move blank tile {}".format(mapp[tuple(generator)]))
            new_board.swapTiles(current_state.blankTileIndex_row, current_state.blankTileIndex_col)
            new_board.parent_state =current_state
            new_board.setMisplacedTilesCount()
            successors.append(new_board)

    return successors

# Using misplaced tiles
# def compare(b1, b2):
#     if b1.misplacedTilesCount > b2.misplacedTilesCount:
#         return 1
#     elif b1.misplacedTilesCount < b2.misplacedTilesCount:
#         return -1
#     return 0

# Using Manhattan distance
def compare(b1, b2):
    if b1.manhattan_distance > b2.manhattan_distance:
        return 1
    elif b1.manhattan_distance < b2.manhattan_distance:
        return -1
    return 0


def best_first_search(initial_state):
    if initial_state.is_goal():
        return initial_state

    initial_state.setMisplacedTilesCount()
    closed = list()
    open = list()
    open.append(initial_state)

    while open:
        state = open.pop(0)
        closed.append(list(state.currentBoard))
        successors = get_successors(state)
        for child in successors:
            if list(child.currentBoard) not in closed:
                if child.is_goal():
                    return child
                open.append(child)

        open = sorted(open, key=cmp_to_key(compare))
    return None


def print_board(board):
    print("+---+---+---+")
    for row in range(3):
        print("|", end="")
        for col in range(3):
            if board[row][col] == 0:
                print("   |", end="")
            else:
                print(" " + str(board[row][col]) + " |", end="")
        print("\n+---+---+---+")


def print_solution(solution):
    path = list()
    path.append(solution)
    parent_state = solution.parent_state
    while parent_state:
        path.append(parent_state)
        parent_state = parent_state.parent_state

    for t in range(len(path)):
        state = path[len(path) - t - 1]
        print(state.blankTileStatus)
        print_board(state.currentBoard)


def main():
    initial_board = [[6, 0, 2], [1, 8, 4], [7, 3, 5]]
    blank_tile_row, blank_tile_col = -1, -1

    for i in range(3):
        for j in range(3):
            if initial_board[i][j] == 0:
                blank_tile_row, blank_tile_col = i, j
                break
        if blank_tile_row > -1:
            break

    ini_state = Board(initial_board, blank_tile_row, blank_tile_col, "Start")

    print_solution(best_first_search(ini_state))


goal_board = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

main()
