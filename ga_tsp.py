import random
import math
from population import Population

""" 目标函数"""


class Fitness:
	city_number = 20
	citys = [[0.96,0.44],[0.65,0.82],[0.25,0.38],[0.63,0.60],[0.50,0.81],[0.52,0.87],[0.62,0.93],[0.20,0.87],[0.27,0.05],[0.70,0.75],[0.82,0.38],[0.39,0.92],[0.58,0.07],[0.77,0.44],[0.31,0.30],[0.40,0.18],[0.82,0.41],[0.57,0.76],[0.90,0.94],[0.19,0.27]]
	@staticmethod
	def value(x):
		sum_ = 0
		for i in range(len(x)):
			if i==0:
				s = x[-1]
			else:
				s = x[i-1]
			e = x[i]

			s = Fitness.citys[s]
			e = Fitness.citys[e]
			sum_+=math.sqrt((s[0]-e[0])*(s[0]-e[0])+(s[1]-e[1])*(s[1]-e[1]))
		return sum_
	@staticmethod
	def plot(route, filename):
		'''

        :param positions: N*2, position of city
        :param route:     N,   route of salesman
        :param filename:  str, file to save
        :return: None
        '''
		positions = Fitness.citys
		import numpy as np
		import matplotlib.pyplot as plt
		plt.cla()
		N = len(positions)
		positions = np.array(positions)

		plt.scatter(positions[:, 0], positions[:, 1])  # plot A
		plt.scatter(positions[:, 0], positions[:, 1])  # plot B
		start_node = route[-1]

		for i in range(N):
			start_pos = positions[start_node]
			next_node = route[i]

			end_pos = positions[next_node]

			plt.annotate("",
						 xy=start_pos, xycoords='data',
						 xytext=end_pos, textcoords='data',
						 arrowprops=dict(arrowstyle="->",
										 connectionstyle="arc3"))

			start_node = next_node

			plt.savefig(filename)


class Individual_TSP:

	def __init__(self,x,mute_rate=0.4):
		self.x = x
		self.y = Fitness.value(self.x)

		self.mute_rate = mute_rate



	@staticmethod
	def init_random_individual():

		route = list(range(Fitness.city_number))
		random.shuffle(route)

		return Individual_TSP(route)

	def __lt__(self, other):
		return self.y<other.y

	def cross_over(self,mate):
		father = self
		mother = mate

		random_cut = random.sample(range(len(father.x)), 1)[0]

		father_cut = father.x[:random_cut]

		father_cut_set = set(father_cut)
		for i in mother.x:
			if i not in father_cut_set:
				father_cut.append(i)
				father_cut_set.add(i)

		return Individual_TSP(father_cut)

	def mutate(self):

		bianyi_idx = random.sample(range(len(self.x)), 2)
		self.x[bianyi_idx[0]], self.x[bianyi_idx[1]] = self.x[bianyi_idx[1]], self.x[bianyi_idx[0]]
		self.y = Fitness.value(self.x)


population = Population(population_size=3000,generation=100,individual_class=Individual_TSP)
population.init_population()
population.evolve()
#
#
Fitness.plot(population.best.x,"result.jpg")
