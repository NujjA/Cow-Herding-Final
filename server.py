from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import CHModel
from random_agent import RandomAgent
from wall import WallAgent
from cow_agent import CowAgent
from plan_agent import PlanAgent
from montecarlo import MonteCarloAgent
from td_agent import TDAgent
from trained_mc_agent import TrainedMonteCarloAgent
import random
import movement_control

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {"Filled": "true"}
    
    if type(agent) is WallAgent:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["Color"] = "red"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    
    elif type(agent) is RandomAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "blue"
        portrayal["r"] = .5
        
    elif type(agent) is CowAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "black"
        portrayal["r"] = .5
    
    elif type(agent) is PlanAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "purple"
        portrayal["r"] = .5

    elif type(agent) is MonteCarloAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "green"
        portrayal["r"] = .5
        
    elif type(agent) is TDAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "orange"
        portrayal["r"] = .5
        
    elif type(agent) is TrainedMonteCarloAgent:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["Color"] = "yellow"
        portrayal["r"] = .5

    return portrayal


### Change number of agents here! ###
random_agents = 0
cow_agents = 4
plan_agents = 2
monte_carlo_agents_trained = 0 # Use pre-trained Q table
monte_carlo_agents_learning = 0 # Only if you want to retrain the Q table
#td_agents = 0
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


server = ModularServer(CHModel,
                       [grid],
                       "Cow Herding Model",
                       {"width": 10, "height": 10,
                        "random_n": random_agents, "cow_n": cow_agents, "plan_n": plan_agents, "mc_n": monte_carlo_agents_learning, "td_n": 0, "t_mc_n": monte_carlo_agents_trained})
