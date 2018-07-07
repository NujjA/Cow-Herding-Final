# Cow Herding Final

## 1. Requirements:
mesa - https://github.com/projectmesa/mesa
numpy
dill

## 2. Runnable files:
run.py - Runs a visualization in the web browser. Probably the best way to see the agents at work. Change the number/type of agents at the bottom of server.py where it says ### Change number of agents here! ###. For best results, please keep teams of two agents since that's what the Q table is trained on.

collect_data.py - This is what I used to collect my data. Runs 3000 episodes with a team of two Random Agents, 3000 episodes with a team of Plan Agents, and 3000 episodes with a team of two Monte Carlo agents. Exports data to csv.

batch_run.py - *DO NOT RUN THIS UNLESS YOU WANT TO RETRAIN THE MONTE CARLO AGENTS* Overwrites previously trained Q table and begins the 

training process over. Trains a team of two Monte Carlo agents for 25,000 episodes, each with 500 timesteps.



## 3. Other files:
montecarlo.py - Agents that perform Monte Carlo learning and build a Q table

trained_mc_agent.py - Agents that use a pre-trained Q table to select actions

random_agent.py - Randomly moving agents

cow_agent.py - Cow Agent behavior

plan_agent.py - Plan following agents

cow_methods.py - Helper methods for cow behavior and interaction

movement_control.py - Agent motion helper methods

rl_methods.py - Helper methods for reinforcement learning

model.py - Builds the environment and places agents in it. Runs the simulation time.

mc_q_save.pkl, mc_q_save.npy - Saved/Trained Q table

wall.py - Wall agents that make up the corral
