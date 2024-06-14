import numpy as np
import networkx as nx
import createGraph

# Initial parameters
class ACOapplication():
    def __init__(self, PHY, K, solution) -> None:
        # the original number of trails, at the start of the simulation
        self.c = 1.0
        # alpha controls the pheromone importance, while beta controls the distance priority
        self.alpha = 1
        self.beta = 5
        # evaporation variable shows the percent how much the pheromone is evaporating in every iteration,
        self.evaporation = 0.5
        # Q provides information about the total amount of pheromone left on the trail by each Ant,
        self.Q = 500
        # antFactor tells us how many ants we’ll use per slices
        self.antFactor = 0.8
        # a little bit of randomness in our simulations
        self.randomFactor = 0.01

        self.PHY = PHY
        self.K = K
        self.solution = solution

        self.numants = len(K)
        self.txy = dict
        self.nxy = dict
        self.deltatxy = dict
        self.positions = dict
        self.road = list

    # Check whether ants can visit node y from node x
    def visitNode(self,x,y) -> bool:
        if (x,y) in self.PHY:
            return True
        else : 
            return False

    # Check the probability for the ant to go from x to y
    def calculateProbability(self,x,y) -> float:
        proba = (pow(self.txy[(x,y)],self.alpha)*pow(self.nxy[(x,y)],self.beta))
        probaall = sum((pow(self.txy[(x,i)],self.alpha)*pow(self.nxy[(x,i)],self.beta)) for i in self.PHY.nodes if (x,i) in self.PHY.edges)
        
        return proba/probaall

    # upgrade txy and nxy each iteration
    def upgradeTxyNxy(self):
        for i in self.PHY.edges:
            self.txy[i] = (1-self.evaporation)*self.txy[i] - sum(self.deltatxy[k][i] for k in self.numants)

    # Calculate deltaTxy
    #def calculateDeltaTxy(self,k,edge):
    #    if k 

    # Main algorithm
    def antColonyAlgo(self):

        # Set up for algorithm
        for k in self.numants:
            self.deltatxy[k] = dict()
            for (x,y) in self.PHY.edges:
                self.deltatxy[k][(x,y)] = 0
        
        for (x,y) in self.PHY.edges:
            self.txy[(x,y)] = self.PHY.nodes[y]['cap']

            self.nxy[(x,y)] = self.PHY.edges[(x,y)]['bandwidth']

        turn = 0
        while (turn < 1000) or (self.Q > 0):
            for k in self.numants:
                maxprob = 0
                for (self.positions[k],y) in self.PHY.edges:
                    if self.calculateProbability(self.positions[k],y) > maxprob:
                        self.positions[k] = y
                        self.deltatxy[(x,y)] = 1/self.PHY.edges[(x,y)]['bandwidth']
                        self.road[k].append(y)

            # Global update
            self.upgradeTxyNxy()

                

                    
