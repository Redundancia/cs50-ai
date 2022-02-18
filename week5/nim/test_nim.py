import nim

def test_get_q_value_empty():
    state = [1,2,3]
    action = (1, 2)
    player = nim.NimAI()
    assert player.get_q_value(state,action) == 0

def test_get_q_value_valid():
    state = [1,2,3]
    action = (1, 2)
    player = nim.NimAI()
    player.q[(tuple(state),action)] = 1
    assert player.get_q_value(state,action) == 1

def test_update_q_value_stored():
    state = [1,2,3]
    action = (1, 2)
    old_q = 0.5
    reward = 1
    future_rewards = 1.2
    player = nim.NimAI()
    player.update_q_value(state, action, old_q, reward, future_rewards) 
    assert player.get_q_value(state,action) == old_q + player.alpha * (reward + future_rewards - old_q)

def test_best_future_reward_valid():
    state = [1,2,3]
    action = (1, 2)
    action2 = (2, 3)
    old_q = 0.5
    reward = 1
    reward2 = 2
    future_rewards = 1.2
    player = nim.NimAI()
    player.update_q_value(state, action, old_q, reward, future_rewards) 
    player.update_q_value(state, action2, old_q, reward2, future_rewards)
    assert player.best_future_reward(state) == player.get_q_value(state,action2)

def test_best_future_reward_no_data():
    state = [1,2,3]
    state_no_q_value = [3,2,1]
    action = (1, 2)
    action2 = (2, 3)
    old_q = 0.5
    reward = 1
    reward2 = 2
    future_rewards = 1.2
    player = nim.NimAI()
    player.update_q_value(state, action, old_q, reward, future_rewards) 
    player.update_q_value(state, action2, old_q, reward2, future_rewards)
    assert player.best_future_reward(state_no_q_value) == 0

def test_best_future_reward_empty():
    state = [1,2,3]
    player = nim.NimAI()
    assert player.best_future_reward(state) == 0

def test_choose_action_valid():
    state = [1,2,3]
    action = (1, 2)
    action2 = (2, 3)
    old_q = 0.5
    reward = 1
    reward2 = 2
    future_rewards = 1.2
    player = nim.NimAI()
    player.update_q_value(state, action, old_q, reward, future_rewards) 
    player.update_q_value(state, action2, old_q, reward2, future_rewards)
    assert player.choose_action(state,epsilon=False) == action2

def test_get_random_action_one():
    state = [0,0,1]
    player = nim.NimAI()
    assert player.get_random_action(state) == (2,1)

def test_choose_action():
    state = [0,0,3]
    player = nim.NimAI()
    action = (1, 2)
    action2 = (2, 3)
    old_q = 0.5
    reward = 1
    reward2 = 2
    future_rewards = 1.2
    player = nim.NimAI()
    player.update_q_value(state, action, old_q, reward, future_rewards) 
    player.update_q_value(state, action2, old_q, reward2, future_rewards)
    assert player.choose_action(state,epsilon=False) == action2