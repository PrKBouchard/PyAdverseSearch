from functools import lru_cache

def maxn(state, depth, players, heuristic):
    """
    state      : état du jeu (doit avoir get_possible_moves, _apply_action, is_game_over)
    depth      : profondeur
    players    : liste des joueurs
    heuristic  : fonction(state) -> liste de scores
    """

    player_index = players.index(state.player)

    key = (str(state.board), state.player, depth)

    if key in maxn._cache:
        return maxn._cache[key]

    if depth == 0 or state.is_game_over():
        result = (heuristic(state), None)
        maxn._cache[key] = result
        return result

    best_score = None
    best_move = None

    moves = state.get_possible_moves()

    moves = sorted(
        moves,
        key=lambda m: heuristic(state._apply_action(m))[player_index] if m else -9999,
        reverse=True
    )

    for move in moves:
        next_state = state._apply_action(move)
        scores, _ = maxn(next_state, depth - 1, players, heuristic)

        if best_score is None or scores[player_index] > best_score[player_index]:
            best_score = scores
            best_move = move

    result = (best_score, best_move)
    maxn._cache[key] = result
    return result


maxn._cache = {}


def choose_move_maxn(state, players, heuristic, depth=3):
    _, move = maxn(state, depth, players, heuristic)

    if move is None:
        return state._apply_action(None)

    return state._apply_action(move)


def reset_cache():
    maxn._cache.clear()
