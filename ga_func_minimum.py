import random
from population import Population
""" 目标函数"""

class Fitness:
	left = 4
	right = 10
	@staticmethod
	def value(x):
		return x*x

class Individual_Minimize:

	def __init__(self,x,mute_size=1,mute_rate=0.25):
		self.x = x
		self.y = Fitness.value(self.x)
		self.mute_size = mute_size
		self.mute_rate = mute_rate



	@staticmethod
	def init_random_individual():
		random_number = Fitness.left + (Fitness.right - Fitness.left) * random.random()

		return Individual_Minimize(random_number)

	def __lt__(self, other):
		return self.y<other.y

	def cross_over(self,mate):

		return Individual_Minimize((self.x+mate.x)/2)

	def mutate(self):
		x_to_edge = min(self.x - Fitness.left, Fitness.right - self.x)

		interval_to_mute = [self.x - x_to_edge, self.x + x_to_edge]

		x = interval_to_mute[0] + random.random() * (interval_to_mute[1] - interval_to_mute[0])

		self.x = x
		self.y = Fitness.value(self.x)

population = Population(population_size=100,generation=100,individual_class=Individual_Minimize)
population.init_population()
population.evolve()




