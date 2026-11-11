"""tictactoe.py: minimax and alpha-beta search for noughts and crosses.

The board is a string of 9 characters: 'X', 'O' or '.'.  X moves first
and maximises the value; O minimises it.  Values: +1 X wins, -1 O wins,
0 draw.
"""
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
         (2, 5, 8), (0, 4, 8), (2, 4, 6)]
count = 0                                # nodes visited


def winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def moves(b):
    return [i for i, c in enumerate(b) if c == "."]


def play(b, i, who):
    return b[:i] + who + b[i + 1:]


def minimax(b, x_to_move):
    global count
    count += 1
    w = winner(b)
    if w or not moves(b):
        return {"X": 1, "O": -1, None: 0}[w]
    vals = [minimax(play(b, i, "X" if x_to_move else "O"), not x_to_move)
            for i in moves(b)]
    return max(vals) if x_to_move else min(vals)


def alphabeta(b, x_to_move, alpha=-2, beta=2):
    global count
    count += 1
    w = winner(b)
    if w or not moves(b):
        return {"X": 1, "O": -1, None: 0}[w]
    for i in moves(b):
        v = alphabeta(play(b, i, "X" if x_to_move else "O"),
                      not x_to_move, alpha, beta)
        if x_to_move:
            alpha = max(alpha, v)
        else:
            beta = min(beta, v)
        if alpha >= beta:
            break                        # the opponent will avoid this line
    return alpha if x_to_move else beta


def best_move(b, x_to_move):
    who = "X" if x_to_move else "O"
    scored = [(alphabeta(play(b, i, who), not x_to_move), i)
              for i in moves(b)]
    return (max if x_to_move else min)(scored)[1]


if __name__ == "__main__":
    for name, f in (("minimax", minimax), ("alpha-beta", alphabeta)):
        count = 0
        v = f("." * 9, True)
        print(f"{name:11} value of empty board = {v:2}, nodes = {count:,}")
    b = "XO.XO...."                      # X to move: where must X play?
    print("\nposition:")
    for r in range(3):
        print("  " + " ".join(b[3 * r:3 * r + 3]))
    print("X's best move is square", best_move(b, True))
