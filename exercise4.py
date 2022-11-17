"""
    Parcial 2 - MOS
    Ejercicio 4

    Realizado por:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
"""

import random
import math

def second_max_min(list, mode):
    if mode == 'max':
        temp_list = [x for x in list if x != max(list)]
        return max(temp_list)
    elif mode == 'min':
        temp_list = [x for x in list if x != min(list)]
        return min(temp_list)

class ZValues:

    def __init__(self, point, z):
        self.point = point
        self.z = z

    def __lt__(self, other):
        return self.z < other.z

    def __gr__(self, other):
        return self.z > other.z

    @classmethod
    def find_z(cls, values, z):
        counter = 0
        for value in values:
            if value.z == z.z:
                return counter
            counter += 1


def simplex(fev_list:list[tuple], z):

    selected_fev = random.choice(fev_list)
    # Create graph
    graph = [[999 for _ in range(len(fev_list))] for _ in range(len(fev_list))]
    i, j = 0, 0
    for x in fev_list:
        for y in fev_list:
            distance = math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))
            if distance == 0:
                distance = 999
            graph[i][j] = distance
            j += 1
        j = 0
        i += 1

    while True:
        index_selected_fev = fev_list.index(selected_fev)
        selected_distances = graph[index_selected_fev]
        closest_fev_distance = min(selected_distances)
        second_closest_distance = second_max_min(selected_distances, 'min')

        closest_index = selected_distances.index(closest_fev_distance)
        second_closest_index = selected_distances.index(second_closest_distance)
        closest_fev = fev_list[closest_index]
        second_closest_fev = fev_list[second_closest_index]

        # Calculate the z value in the point
        selected_z = z(selected_fev[0], selected_fev[1])
        closest_z = z(closest_fev[0], closest_fev[1])
        second_closest_z = z(second_closest_fev[0], second_closest_fev[1])

        z_list = [ZValues(selected_fev, selected_z), ZValues(closest_fev, closest_z), ZValues(second_closest_fev, second_closest_z)]

        best_z = max(z_list)

        index = ZValues.find_z(z_list, best_z)
        if index == 0:
            return selected_fev, selected_z
        selected_fev = best_z.point

def objective_function(x, y):
    return 3*x + 2*y

result = simplex([(0,0), (40,0), (40,20), (20,60), (0, 80)], objective_function)
print(result)
