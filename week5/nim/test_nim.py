import nim

def test_get_q_value_empty():
    state = [1,2,3]
    action = 1
    player = nim.NimAI()
    assert player.get_q_value(state,action) == 0

def test_get_q_value_valid():
    state = [1,2,3]
    action = 1
    player = nim.NimAI()
    player.q[(tuple(state),action)] = 1
    assert player.get_q_value(state,action) == 1