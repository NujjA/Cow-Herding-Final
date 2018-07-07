from model import CHModel
import csv, datetime

# number of episodes
episodes = 3000
# number of steps per episode
steps = 100

# number of agents
random_agents = 2
cow_agents = 4
plan_agents = 2
trained_mc_agents = 2

# Collect times for random_agents
final_random_scores = []
final_random_times = []

for episode in range(episodes):
    model = CHModel(10, 10, cow_n = cow_agents, random_n = random_agents, episode_number = episode)

    print("Random Episode ", episode)
    for i in range(steps):
        model.step()
        # if the agents are able to herd the cows in the given number of timesteps, save the time finished
        if(model.done):
            final_random_times.append(i)
            #save the final score
            final_random_scores.append(model.score)
    # if the agents were not able to herd the cows in the given number of timesteps, save the maximum time allowed and the end score
    if (not(model.done)):
        final_random_times.append(steps)
        final_random_scores.append(model.score)

# Collect times for plan_agents
final_plan_scores = []
final_plan_times = []
for episode in range(episodes):
    model = CHModel(10, 10, cow_n = cow_agents, plan_n = plan_agents, episode_number = episode)

    print("Plan Episode ", episode)
    for i in range(steps):
        model.step()
        # if the agents are able to herd the cows in the given number of timesteps, save the time finished
        if(model.done):
            final_plan_times.append(i)
            #save the final score
            final_plan_scores.append(model.score)
    # if the agents were not able to herd the cows in the given number of timesteps, save the maximum time allowed
    if (not(model.done)):
        final_plan_times.append(steps)
        final_plan_scores.append(model.score)

# Collect times for trained monte carlo agents
final_mc_scores = []
final_mc_times = []
for episode in range(episodes):
    model = CHModel(10, 10, cow_n = cow_agents, t_mc_n = trained_mc_agents, episode_number = episode)

    print("Monte Carlo Episode ", episode)
    for i in range(steps):
        model.step()
        # if the agents are able to herd the cows in the given number of timesteps, save the time finished
        if(model.done):
            final_mc_times.append(i)
            #save the final score
            final_mc_scores.append(model.score)
    # if the agents were not able to herd the cows in the given number of timesteps, save the maximum time allowed
    if (not(model.done)):
        final_mc_times.append(steps)
        final_mc_scores.append(model.score)
        
# Save collected data to CSV
csv_name = datetime.datetime.now().strftime("%y_%m_%d_%H_%M") + "_save.csv"
with open(csv_name, 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(["RandomScore", "RandomTime", "PlanScore", "PlanTime", "MCScore", "MCTime"])
    for i in range(episodes):
        thewriter.writerow([final_random_scores[i], final_random_times[i], final_plan_scores[i], final_plan_times[i], final_mc_scores[i], final_mc_times[i]])
