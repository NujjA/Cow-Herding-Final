from mesa import Agent, Model
import random
import movement_control, cow_methods
import numpy as np

class PlanAgent(Agent):
    """ An agent that follows plan of JIAC V team by Heβler et al. (2010) """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("creating plan agent")
        
        
        # plan steps
        # look for cloeset cow to goal
        self.LOOKFORCOW = 0
        # herd cow
        self.HERDCOW = 1
        
        self.vision_radius = 2 # How far the agent can see
        
        self.current_plan_step = 0
        self.cow_to_follow = None

    def step(self):
        print("plan agent step")
        self.move()

    def move(self):
        prev_pos = self.pos
        #possible_steps = movement_control.find_empty_location(self.pos, self.model)
        #new_position = random.choice(possible_steps)
        #self.model.grid.move_agent(self, new_position)
        
        if (self.current_plan_step == self.LOOKFORCOW):
            print("finding cow to follow")
            self.cow_to_follow = self.find_free_cow_in_radius()
            if (self.cow_to_follow is not None):
                print("found cow")
                self.current_plan_step = self.HERDCOW
            else:
                # Move randomly to find a cow
                print("no cow here, keep looking")
                possible_steps = movement_control.find_empty_location(self.pos, self.model)
                new_position = random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)
        elif (self.current_plan_step == self.HERDCOW):
            
            if not self.cow_to_follow: # if no cow to follow, go back to looking
                self.current_plan_step = self.LOOKFORCOW
            elif self.cow_to_follow.pos in self.model.goalState: # cow is already in goal
                print("cow is in the goal - resetting")
                self.current_plan_step = self.LOOKFORCOW
                self.cow_to_follow = None
            else:
                # herd the cow!
                print("herding cow")
                self.move_to_herding_location()
                
        if prev_pos == self.pos: # if hasn't moved, might be stuck, move randomly
            possible_steps = movement_control.find_empty_location(self.pos, self.model)
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

                
                
    def move_to_herding_location(self):
        target_pos = None
        goal_pos = self.model.goalTarget # for clarity when reading code
        cow_pos = self.cow_to_follow.pos # for clarity when reading code
        
        #if goal is greater y than cow
        if movement_control.is_greater_y(goal_pos, cow_pos):
            target_pos = (cow_pos[0], cow_pos[1]-1)

        #if goal is smaller y than cow
        elif movement_control.is_smaller_y(goal_pos, cow_pos):
            target_pos = (cow_pos[0], cow_pos[1]+1)
            
        #if goal is greater x than cow
        elif movement_control.is_greater_x(goal_pos, cow_pos):
            target_pos = (cow_pos[0]-1, cow_pos[1])

        #if goal is smaller x than cow
        elif movement_control.is_smaller_x(goal_pos, cow_pos):
            target_pos = (cow_pos[0]+1, cow_pos[1])
            
        if target_pos:
            target_pos = self.model.grid.torus_adj(target_pos)
            movement_control.move_towards(self, target_pos)
            
        print("moving towards ", target_pos)
        #self.pos
            
        
    def find_free_cow_in_radius(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center=False, radius= self.vision_radius)
        cows_in_radius = cow_methods.find_neighbor_cows(neighbors)
        free_cows = []
        for cow in cows_in_radius:
            if (not(cow in self.model.goalState)):
                free_cows.append(cow)
        return self.find_closest_cow_to_goal(free_cows)

        
    def find_closest_cow_to_goal(self, free_cows):
        if not free_cows:
            return None
        
        closest_cow = None
        closest_distance = np.inf
        for cow in free_cows:
            current_distance = movement_control.get_distance(self.model.grid, cow.pos, self.model.goalTarget)
            if (current_distance < closest_distance):
                closest_distance = current_distance
                closest_cow = cow
        return closest_cow
