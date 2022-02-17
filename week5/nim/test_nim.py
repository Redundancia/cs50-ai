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

def test_update_q_value_stored():
    state = [1,2,3]
    action = 1
    old_q = 0.5
    reward = 1
    future_rewards = 1.2
    player = nim.NimAI()
    player.update_q_value(state, action, old_q, reward, future_rewards) 
    assert player.get_q_value(state,action) == old_q + player.alpha * (reward + future_rewards - old_q)