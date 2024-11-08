import traci
import numpy as np
import random

# Q-learning parameters
ALPHA = 0.1       # Learning rate
GAMMA = 0.9       # Discount factor
EPSILON = 0.1     # Exploration rate

NBR_EPISODES = 1000
STEPS_PER_EPISODE = 3600    # 1 hour simulation steps

# Environment parameters
STATE_SPACE_SIZE = 2  # (ramp_queue, main_queue) Define based on the range of possible states
ACTION_SPACE_SIZE = 3  # (SetPhaseDuration 10, SetPhaseDuration 20, SetPhaseDuration 30) Define the number of actions (e.g., different green light durations)

# Initialize Q-table [rows: States; columns: Actions]
q_table = np.zeros((STATE_SPACE_SIZE, ACTION_SPACE_SIZE))


def choose_action(state):
    """Choose action using epsilon-greedy policy."""
    if random.uniform(0, 1) < EPSILON:
        return random.randint(0, ACTION_SPACE_SIZE - 1)     # Exploration: choose a random action
    else:
        return np.argmax(q_table[state])                    # Exploitation: choose the best action based on Q-table


def get_state():
    """Retrieve the current state from SUMO."""
    # Example: measure number of vehicles in specific lanes
    ramp_queue = traci.lane.getLastStepVehicleNumber("E8_0")  # Replace with your lane ID for the ramp
    main_queue = traci.lane.getLastStepVehicleNumber("E6_0") + traci.lane.getLastStepVehicleNumber("E6_1") + traci.lane.getLastStepVehicleNumber("E6_2")
    current_state = (ramp_queue, main_queue)    # Modify based on your state representation
    return current_state  


def take_action(action):
    """Apply action in SUMO."""
    if action == 0:
        # Short green phase
        traci.trafficlight.setPhaseDuration("J11", 10)      # setPhaseDuration(tlsID, phaseDuration): Set the remaining phase duration of the current phase in seconds. This value has no effect on subsquent repetitions of this phase.
    elif action == 1:
        # Medium green phase
        traci.trafficlight.setPhaseDuration("J11", 20)
    elif action == 2:
        # Long green phase
        traci.trafficlight.setPhaseDuration("J11", 30)


def calculate_reward(state):
    """Calculate reward based on the current state."""
    ramp_queue, main_queue = state
    return - (ramp_queue + main_queue)  # Example: penalize based on queue length



def update_q_table(state, action, reward, next_state):
    """Update Q-table based on Q-learning formula."""
    best_next_action = np.argmax(q_table[next_state])
    q_table[state][action] = q_table[state][action] + ALPHA * (reward + GAMMA * q_table[next_state][best_next_action] - q_table[state][action])



# Main training loop
def q_learning(nbr_episodes = NBR_EPISODES):
    for episode in range(NBR_EPISODES):
        traci.start(["sumo", "-c", "../config/my_simulation.sumocfg"])
        state = get_state()
        total_reward = 0
        
        for step in range(STEPS_PER_EPISODE):  # 1-hour simulation, adjust as needed
            action = choose_action(state)
            take_action(action)
            traci.simulationStep()
            
            next_state = get_state()
            reward = calculate_reward(next_state)
            
            update_q_table(state, action, reward, next_state)
            
            state = next_state
            total_reward += reward
        
        print(f"Episode {episode + 1}: Total Reward: {total_reward}")
        
        traci.close()

    policy = np.argmax(q_table, axis=2)
    return policy


# policy_q_learning = q_learning(NBR_EPISODES)