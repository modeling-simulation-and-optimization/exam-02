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
    """Find the second max or min value in a list

    Args:
        list (list): List to be evaluated
        mode (str): 'max' or 'min' to find the second max or min value

    Returns:
        Object: Value found
    """

    if mode == 'max':
        temp_list = [x for x in list if x != max(list)]
        return max(temp_list)
    elif mode == 'min':
        temp_list = [x for x in list if x != min(list)]
        return min(temp_list)

class ZValues:
    """Simple class to manage points and z values
    """
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
    graph = [[9999 for _ in range(len(fev_list))] for _ in range(len(fev_list))]

    # Fill graph with connected nodes
    graph[0][1] = 1
    graph[0][4] = 1

    graph[1][2] = 1

    graph[2][3] = 1

    graph[3][4] = 1

    # Fill the connected nodes with the distance between them
    for i in range(len(fev_list)):
        for j in range(len(fev_list)):
            if graph[i][j] == 1:
                graph[j][i] = 1
                distance = math.sqrt((fev_list[i][0] - fev_list[j][0])**2 + (fev_list[i][1] - fev_list[j][1])**2)
                graph[i][j] = distance
                graph[j][i] = distance
    while True:
        # Find the adjacent nodes to the selected one
        index_selected_fev = fev_list.index(selected_fev)
        selected_distances = graph[index_selected_fev]
        closest_fev_distance = min(selected_distances)
        second_closest_distance = second_max_min(selected_distances, 'min')

        closest_index = selected_distances.index(closest_fev_distance)
        second_closest_index = selected_distances.index(second_closest_distance)
        closest_fev = fev_list[closest_index]
        second_closest_fev = fev_list[second_closest_index]

        # Calculate the z value in each point
        selected_z = z(selected_fev[0], selected_fev[1])
        closest_z = z(closest_fev[0], closest_fev[1])
        second_closest_z = z(second_closest_fev[0], second_closest_fev[1])

        z_list = [ZValues(selected_fev, selected_z), ZValues(closest_fev, closest_z), ZValues(second_closest_fev, second_closest_z)]

        # Find the z value which has the best z value (greatest value)
        best_z = max(z_list)

        # Find the index of said z value and checking if it is the selected one, if it is, then the algorithm is done
        index = ZValues.find_z(z_list, best_z)
        if index == 0:
            return selected_fev, selected_z
        # If it is not, then the new selected node is the one with the best z value found and the process is repeated
        selected_fev = best_z.point

def objective_function(x, y):
    """Objective function to be evaluated (Specific to this problem)"""
    return 3*x + 2*y

if __name__ == "__main__":
    result = simplex([(0,0), (40,0), (40,20), (20,60), (0, 80)], objective_function)
    print(f"The best point is: {result[0]} with a z value of {result[1]}")
