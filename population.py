import random
import copy
class Population:
	def __init__(self,population_size,generation,individual_class):
		self.population_size = population_size
		self.generation  =generation

		self.individual_class = individual_class



	def init_population(self):
		self.population = set()

		while len(self.population) < self.population_size:
			self.population.add(self.individual_class.init_random_individual())


	def evolve(self):
		for step in range(self.generation):



			sorted_population = sorted(self.population)

			self.best = copy.deepcopy(sorted_population[0])
			print(self.best.x)
			print("step {}:".format(step), sorted_population[0].y)

			# 适者生存
			selected = sorted_population[:self.population_size // 2]


			population = set(selected)

			# 繁衍
			while len(population) < self.population_size:
				parants = random.sample(selected, 2)
				child = parants[0].cross_over(parants[1])

				population.add(child)


			# 变异
			for idx,x in enumerate(population):

				if random.random() < x.mute_rate:
					x.mutate()


			self.population = population

