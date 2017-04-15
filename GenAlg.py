import random
import math

class Genome:
    def __init__(self, weights, fitness):
        self.weights = weights
        self.fitness = fitness
        # self.score = 0
    # def __init__(self):
    #     self.weights = []
    #     self.fitness = 0.0

    def getFitness(self):
        return self.fitness

    def copy(self):
        return Genome(list(self.weights) ,self.fitness)

    def __eq__(self, other):
        for i in range(len(self.weights)):
            if math.fabs(self.weights[i] - other.weights[i]) <= 0.001 :
                continue
            else:
                return False
        return True

    def __hash__(self):
        return hash(tuple(self.weights))

class GenAlg:
    mutationRate = 0.05 # up to 0.3
    crossoverRate = 0.7
    popSize = 200
    chromoLength = 2*9 + 3
    maxPerturbation = 0.3
    numElite = 4
    numCopiesElite = 2

    def __init__(self):
        self.population = []
        self.totalFitness = 0.0
        # self.totalScore = 0.0
        self.cGeneration = 0

        for i in range(GenAlg.popSize):
            self.population.append(Genome([random.uniform(-1, 1) for i in range(GenAlg.chromoLength)], 0.0))

    def __iter__(self):
        return iter(self.population)

    def Mutate(self, weights):
        for i in range(len(weights)):
            if (random.uniform(0,1) < GenAlg.mutationRate):
                weights[i] += (random.uniform(-1,1) * GenAlg.maxPerturbation)

    def Roulette(self):
        self.totalFitness = 0
        for genome in self.population:
            self.totalFitness += genome.fitness

        slice = float(random.uniform(0,1) * self.totalFitness)

        fitnessSoFar = 0

        for genome in self.population:
            fitnessSoFar += genome.fitness
            if (fitnessSoFar >= slice):
                return genome.weights

    def Crossover(self, mom, dad, baby1, baby2):
        if ((random.uniform(0,1) > GenAlg.crossoverRate) or (set(mom) == set(dad))):
            baby1 += mom
            baby2 += dad
        else:
            cp = random.randint(0, GenAlg.chromoLength - 1)

            baby1 += mom[0:cp] + dad[cp:GenAlg.chromoLength + 1]
            baby2 += dad[0:cp] + mom[cp:GenAlg.chromoLength + 1]


    def GrabNBest(self, nBest, numCopies, population):
        # sort the population (for scaling and elitism)
        self.population.sort(key=Genome.getFitness)
        while (nBest > 0):
            if self.population[-nBest].fitness > 100:
                self.population[-nBest].fitness = 0.0
                for i in range(numCopies):
                    population.append(self.population[-nBest].copy())
            nBest -= 1

    def Fitness(self, ex, res):
        # dist = math.hypot(ex[0] - res[0], ex[1] - res[1])
        # return 1/(dist + 1)
        # if math.fabs(ex - res) == 1.0:
        #     return 0.0
        # return 1.0
        return 1 / (math.fabs(ex - res) + 1)

    def Epoch(self):

        # create a temporary vector to store new chromosones
        newPop = []
        # Now to add a little elitism we shall add in some copies of the
        # fittest genomes. Make sure we add an EVEN number or the roulette
        # wheel sampling will crash
        if (GenAlg.numCopiesElite * GenAlg.numElite % 2 == 0):
            self.GrabNBest(GenAlg.numElite, GenAlg.numCopiesElite, newPop)

        # now we enter the GA loop

        # repeat until a new population is generated
        while (len(newPop) < GenAlg.popSize):
             # grab two chromosones
            mum = self.Roulette()
            dad = self.Roulette()

            # create some offspring via crossover
            baby1 = list()
            baby2 = list()

            self.Crossover(mum, dad, baby1, baby2)

            # now we mutate
            self.Mutate(baby1)
            self.Mutate(baby2)

            # now copy into vecNewPop population
            newPop.append(Genome(list(baby2), 0.0))
            newPop.append(Genome(list(baby1), 0.0))

       # finished so assign new pop back into m_vecPop
        self.population = newPop
        self.cGeneration += 1
