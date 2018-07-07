from model import CHModel
import movement_control, rl_methods
import numpy as np
import dill

episodes = 25000
steps = 500

# Number of each type of agent to run
random_agents = 0
cow_agents = 4
plan_agents = 0
monte_carlo_agents = 2
trained_mc_agents = 0
td_agents = 0
nA = len(rl_methods.action_space)

MC_Q_values = None # Save Q values so MC agents can access each episode

final_scores = []
for episode in range(episodes):
    model = CHModel(10, 10, random_n = random_agents, cow_n = cow_agents, plan_n = plan_agents, mc_n = monte_carlo_agents, td_n = td_agents, t_mc_n = trained_mc_agents, episode_number = episode, old_Q_values = MC_Q_values)
    print("Episode ", episode)
    for i in range(steps):
        model.step()
        if(model.done):
            print("all cows herded in batch run, breaking")
            break
    final_scores.append(movement_control.compute_score(model))
    MC_Q_values = model.get_new_Q_values()



# Save shared or first Q table for trained MC agent use
if (monte_carlo_agents > 0) :
    print("Saving Q table")
    #Q_to_save = np.asarray(MC_Q_values[0])
    Q_to_save = MC_Q_values[0]
    with open('mc_q_save.pkl', 'wb') as file:
        dill.dump(Q_to_save, file)
    print("Dumped")
