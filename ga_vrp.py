from population import Population
import random
import math
from vrp_input import city_number,citys,loads,capacity,max_cars,center

class Fitness:
    city_number = city_number
    citys = citys
    loads = loads
    capacity = capacity
    max_cars = max_cars
    center = center



    penalty_of_subroute = 5
    citys.append(center)

    @staticmethod
    def split_routes(x):

        sub_routes = []
        sub_route = []
        for city in x:
            if city!=-1:
                sub_route.append(city)
            elif len(sub_route)!=0:

                sub_route+=[len(Fitness.citys)-1]
                sub_routes.append(sub_route)
                sub_route = []
        if len(sub_route)!=0:
            sub_route+=[len(Fitness.citys)-1]
            sub_routes.append(sub_route)
        return sub_routes
    @staticmethod
    def value(x):
        sub_routes = Fitness.split_routes(x)
        for sub_route in sub_routes:

            if sum([Fitness.loads[x] for x in sub_route[:-1]])>Fitness.capacity:
                return -1

        total_sum = Fitness.penalty_of_subroute*len(sub_routes)
        for sub_route in sub_routes:
            sum_ = 0
            for i in range(len(sub_route)):
                if i == 0:
                    s = sub_route[-1]
                else:
                    s = sub_route[i - 1]
                e = sub_route[i]

                s = Fitness.citys[s]
                e = Fitness.citys[e]
                sum_ += math.sqrt((s[0] - e[0]) * (s[0] - e[0]) + (s[1] - e[1]) * (s[1] - e[1]))
            total_sum+=sum_

        return total_sum

    @staticmethod
    def plot(route, filename):
        '''

        :param positions: N*2, position of city
        :param route:     N,   route of salesman
        :param filename:  str, file to save
        :return: None
        '''



        sub_routes = Fitness.split_routes(route)




        positions = Fitness.citys
        import numpy as np
        import matplotlib.pyplot as plt
        plt.cla()

        positions = np.array(positions)


        plt.scatter([Fitness.citys[-1][0]], [Fitness.citys[-1][1]],s=50,c='g')  # plot A

        plt.scatter(positions[:-1, 0], positions[:-1, 1])  # plot A
        plt.scatter(positions[:-1, 0], positions[:-1, 1])  # plot B


        for route in sub_routes:
            start_node = route[-1]
            N = len(route)
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


class Individual_VRP:

    def __init__(self,x,mute_rate=0.4,max_subroutes=10):
        self.x = x
        self.y = Fitness.value(self.x)

        self.mute_rate = mute_rate

        self.max_subroutes = max_subroutes


    @staticmethod
    def init_random_individual():



        route = list(range(Fitness.city_number))+[-1]*Fitness.max_cars

        random.shuffle(route)

        value = Fitness.value(route)
        if value!=-1:

            return Individual_VRP(route)
        else:
            return Individual_VRP.init_random_individual()


    def __lt__(self, other):
        return self.y<other.y

    def cross_over(self,mate):
        father = self
        mother = mate

        random_cut = random.sample(range(len(father.x)), 1)[0]

        father_cut = father.x[:random_cut]

        father_cut_set = set(father_cut)


        father_cut_cars = 0
        for i in father_cut:
            if i==-1:
                father_cut_cars+=1

        for i in mother.x:
            if i==-1 and father_cut_cars<Fitness.max_cars:
                father_cut.append(i)
                father_cut_set.add(i)
                father_cut_cars+=1
            elif i not in father_cut_set:
                father_cut.append(i)
                father_cut_set.add(i)

        value = Fitness.value(father_cut)
        if value!=-1:
            return Individual_VRP(father_cut)
        else:
            return self.cross_over(mate)


    def mutate(self):

        bianyi_idx = random.sample(range(len(self.x)), 2)

        x_temp = list(self.x)
        x_temp[bianyi_idx[0]], x_temp[bianyi_idx[1]] = x_temp[bianyi_idx[1]], x_temp[bianyi_idx[0]]


        value = Fitness.value(x_temp)
        if value!=-1:
            self.x = x_temp
            self.y = value
        else:
            self.mutate()

population = Population(population_size=3000,generation=100,individual_class=Individual_VRP)
population.init_population()
population.evolve()
#
#
Fitness.plot(population.best.x,"result.jpg")
