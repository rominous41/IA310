import math
import random
import numpy as np
from collections import defaultdict

import uuid
import mesa
import numpy
import pandas
from mesa import space
from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.modules import ChartModule

class ContinuousCanvas(VisualizationElement):
    local_includes = [
        "./js/simple_continuous_canvas.js",
    ]

    def __init__(self, canvas_height=500,
                 canvas_width=500, instantiate=True):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.identifier = "space-canvas"
        if (instantiate):
            new_element = ("new Simple_Continuous_Module({}, {},'{}')".
                           format(self.canvas_width, self.canvas_height, self.identifier))
            self.js_code = "elements.push(" + new_element + ");"

    def portrayal_method(self, obj):
        return obj.portrayal_method()

    def render(self, model):
        representation = defaultdict(list)
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            if portrayal:
                portrayal["x"] = ((obj.pos[0] - model.space.x_min) /
                                  (model.space.x_max - model.space.x_min))
                portrayal["y"] = ((obj.pos[1] - model.space.y_min) /
                                  (model.space.y_max - model.space.y_min))
            representation[portrayal["Layer"]].append(portrayal)
        return representation

def wander(x, y, speed, model):
    r = random.random() * math.pi * 2
    new_x = max(min(x + math.cos(r) * speed, model.space.x_max), model.space.x_min)
    new_y = max(min(y + math.sin(r) * speed, model.space.y_max), model.space.y_min)

    return new_x, new_y

def can_attack(pos1,pos2,distance_attack):
    if (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2<distance_attack:
        return True
    else:
        return False

def get_healthy_villager(model):
    count=0
    for agent in model.schedule.agents:
        if agent.dead==False and agent.lycanthrope==False:
            count+=1
    return count

def get_lycanthropes(model):
    count=0
    for agent in model.schedule.agents:
        if agent.dead==False and agent.lycanthrope==True:
            count+=1
    return count

def get_transformed_lycanthropes(model):
    count=0
    for agent in model.schedule.agents:
        if agent.dead==False and agent.transforme==True:
            count+=1
    return count

def get_n_agents(model):
    count=0
    for agent in model.schedule.agents:
        if agent.dead==False :
            count+=1
    return count

class  Village(mesa.Model):
    def  __init__(self,  n_villagers,n_lycanthropes=5,n_clerics=1,n_hunters=2):
        mesa.Model.__init__(self)
        self.space = mesa.space.ContinuousSpace(600, 600, False)
        self.schedule = RandomActivation(self)
        for  i  in  range(n_villagers):
            lycanthrope=i<n_lycanthropes
            self.schedule.add(Villager(random.random()  *  600,  random.random()  *  600,  10, uuid.uuid1(), self,lycanthrope=lycanthrope))
        for i in range(n_clerics):
            self.schedule.add(Cleric(random.random()  *  600,  random.random()  *  600,  10, uuid.uuid1(), self))
        for i in range(n_hunters):
            self.schedule.add(Hunter(random.random()  *  600,  random.random()  *  600,  10, uuid.uuid1(), self))

        self.datacollector = DataCollector(
            model_reporters={"n_healthy_villager": get_healthy_villager,"n_lycanthropes": get_lycanthropes,"n_transformed_lycanthropes": get_transformed_lycanthropes,"n_agents":get_n_agents}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        if self.schedule.steps >= 10000:
            self.running = False


class Cleric(mesa.Agent):
    def __init__(self, x, y, speed, unique_id: int, model: Village, distance_attack=40, p_attack=0.6,lycanthrope=False):
        super().__init__(unique_id, model)
        self.pos = (x, y)
        self.speed = speed
        self.model = model
        self.distance_attack = distance_attack
        self.p_attack = p_attack
        self.lycanthrope=lycanthrope
        self.transforme=False
        self.dead=False

    def portrayal_method(self):
        color = "green"
        if self.lycanthrope:
            color = "red"
        if self.transforme:
            r=6
        else:
            r = 3
        if self.dead:
            r=0
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": color,
                     "r": r}
        return portrayal

    def step(self):
        if self.dead==False:
            self.pos = wander(self.pos[0], self.pos[1], self.speed, self.model)
            if random.random()<0.1 and self.lycanthrope:
                self.transforme=True
            if self.transforme:
                for agent in self.model.schedule.agents:
                    if can_attack(self.pos,agent.pos,40):
                        agent.lycanthrope=True
            else:
                for agent in self.model.schedule.agents:
                    if can_attack(self.pos,agent.pos,30) and agent.transforme==False:
                        agent.lycanthrope=False

class Hunter(mesa.Agent):
    def __init__(self, x, y, speed, unique_id: int, model: Village, distance_attack=40, p_attack=0.6,lycanthrope=False):
        super().__init__(unique_id, model)
        self.pos = (x, y)
        self.speed = speed
        self.model = model
        self.distance_attack = distance_attack
        self.p_attack = p_attack
        self.lycanthrope=lycanthrope
        self.transforme=False
        self.dead=False

    def portrayal_method(self):
        color = "black"
        if self.lycanthrope:
            color = "red"
        if self.transforme:
            r=6
        else:
            r = 3
        if self.dead:
            r=0
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": color,
                     "r": r}
        return portrayal

    def step(self):
        if self.dead==False:
            self.pos = wander(self.pos[0], self.pos[1], self.speed, self.model)
            if random.random()<0.1 and self.lycanthrope:
                self.transforme=True
            if self.transforme:
                for agent in self.model.schedule.agents:
                    if can_attack(self.pos,agent.pos,40):
                        agent.lycanthrope=True
            else:
                for agent in self.model.schedule.agents:
                    if can_attack(self.pos,agent.pos,40) and agent.transforme==True:
                        #self.schedule.remove(agent)
                        agent.dead=True

class Villager(mesa.Agent):
    def __init__(self, x, y, speed, unique_id: int, model: Village, distance_attack=40, p_attack=0.6,lycanthrope=False):
        super().__init__(unique_id, model)
        self.pos = (x, y)
        self.speed = speed
        self.model = model
        self.distance_attack = distance_attack
        self.p_attack = p_attack
        self.lycanthrope=lycanthrope
        self.transforme=False
        self.dead=False

    def portrayal_method(self):
        color = "blue"
        if self.lycanthrope:
            color = "red"
        if self.transforme:
            r=6
        else:
            r = 3
        if self.dead:
            r=0
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": color,
                     "r": r}
        return portrayal

    def step(self):
        if self.dead==False:
            self.pos = wander(self.pos[0], self.pos[1], self.speed, self.model)
            if random.random()<0.1 and self.lycanthrope:
                self.transforme=True
            if self.transforme:
                for agent in self.model.schedule.agents:
                    if can_attack(self.pos,agent.pos,40):
                        agent.lycanthrope=True

chart = ChartModule([{"Label": "n_healthy_villager",
                      "Color": "blue"},{"Label": "n_lycanthropes",
                      "Color": "red"},{ "Label": "n_transformed_lycanthropes",
                      "Color": "green"},{"Label": "n_agents",
                      "Color": "black"}],data_collector_name='datacollector')


if  __name__  ==  "__main__":
    #server  =  ModularServer(Village, [ContinuousCanvas(),chart],"Village",{"n_villagers":  20,"n_lycanthropes": 5,"n_clerics":1,"n_hunters":2})

    server  =  ModularServer(Village, [ContinuousCanvas(),chart],"Village",{"n_villagers":  mesa.visualization.ModularVisualization.UserSettableParameter('slider',
"healthy villagers", 20, 5, 40, 1),"n_lycanthropes": mesa.visualization.ModularVisualization.UserSettableParameter('slider',
"lycanthropes", 5, 5, 20, 1),"n_clerics":mesa.visualization.ModularVisualization.UserSettableParameter('slider',"clerics", 1, 0, 20, 1),"n_hunters":mesa.visualization.ModularVisualization.UserSettableParameter('slider',"hunters", 2, 0, 20, 1)})
    server.port = 8521
    #server.launch()

    fixed_params = {
    "n_villagers": 50,
    "n_lycanthropes": 5,
    "n_hunters":1
    }

    variable_params = {"n_clerics": range(0, 6, 1)}

    batch_run = BatchRunner(
    Village,
    variable_params,
    fixed_params,
    max_steps=1000,
    model_reporters={"n_healthy_villager": get_healthy_villager,"n_lycanthropes": get_lycanthropes,"n_transformed_lycanthropes": get_transformed_lycanthropes,"n_agents":get_n_agents}
    )
    batch_run.run_all()
    df=batch_run.get_model_vars_dataframe()
    with pandas.option_context('display.max_rows', None,'display.max_columns', None,
    'display.precision', 3,):
        print(df)

