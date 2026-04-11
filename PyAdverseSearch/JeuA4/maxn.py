# maxn.py

def heuristic_scores(state, players):
    raw_scores = state.get_scores()
    scores = raw_scores[:]

    size = len(state.board)
    center = size // 2

    for i, p in enumerate(players):
        temp_state = state.__class__(state.board, p)
        mobility = len([m for m in temp_state.get_possible_moves() if m])
        scores[i] += 2 * mobility

    for r in range(size):
        for c in range(size):
            cell = state.board[r][c]
            if cell in players:
                i = players.index(cell)
                dist = abs(r - center) + abs(c - center)
                scores[i] += max(0, 6 - dist)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for r in range(size):
        for c in range(size):
            cell = state.board[r][c]
            if cell in players:
                i = players.index(cell)

                adjacent = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size:
                        if state.board[nr][nc] == cell:
                            adjacent += 1

                if adjacent == 0:
                    scores[i] -= 3

    return scores


def maxn(state, depth, players):
    if depth == 0 or state.is_terminal():
        return heuristic_scores(state, players), None

    current_player = state.player
    player_index = players.index(current_player)

    best_score = None
    best_move = None

    for move in state.get_possible_moves():
        next_state = state.apply_action(move)
        scores, _ = maxn(next_state, depth - 1, players)

        if best_score is None or scores[player_index] > best_score[player_index]:
            best_score = scores
            best_move = move

    return best_score, best_move


def choose_move(state, players, depth=3):
    scores, move = maxn(state, depth, players)

    if move is None:
        return state.apply_action(None)

    return state.apply_action(move)