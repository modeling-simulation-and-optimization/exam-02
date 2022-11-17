"""
    Parcial 2 - MOS
    Ejercicio 1

    Realizado por:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
"""

import matplotlib.pyplot as plt

from pyomo.environ import *
from pyomo.opt import SolverFactory


def delete_component(Model, comp_name):
    list_del = [vr for vr in vars(Model)
                if comp_name == vr
                or vr.startswith(comp_name + '_index')
                or vr.startswith(comp_name + '_domain')]

    list_del_str = ', '.join(list_del)
    print('Deleting model components ({}).'.format(list_del_str))

    for kk in list_del:
        Model.del_component(kk)


Model = ConcreteModel()

Model.Nodes = RangeSet(1, 5)

Model.Hops = Param(Model.Nodes, Model.Nodes, mutable=True)
Model.Costs = Param(Model.Nodes, Model.Nodes, mutable=True)

for i in Model.Nodes:
    for j in Model.Nodes:
        Model.Hops[i, j] = 999
        Model.Costs[i, j] = 999

Model.Hops[1, 2] = 1
Model.Hops[1, 3] = 1
Model.Hops[2, 5] = 1
Model.Hops[3, 4] = 1
Model.Hops[4, 5] = 1

Model.Costs[1, 2] = 10
Model.Costs[1, 3] = 5
Model.Costs[2, 5] = 10
Model.Costs[3, 4] = 5
Model.Costs[4, 5] = 5

Model.X = Var(Model.Nodes, Model.Nodes, domain=Binary)

Model.f1 = sum(Model.Hops[i, j] * Model.X[i, j] for i in Model.Nodes for j in Model.Nodes)
Model.f2 = sum(Model.Costs[i, j] * Model.X[i, j] for i in Model.Nodes for j in Model.Nodes)

Model.obj = Objective(expr=Model.f2, sense=minimize)


# Restricción nodo origen
def source_restriction(Model, i):
    if i == 1:
        return sum(Model.X[i, j] for j in Model.Nodes) == 1
    else:
        return Constraint.Skip


Model.source = Constraint(Model.Nodes, rule=source_restriction)


# Restricción nodo destino
def destination_restriction(Model, j):
    if j == 5:
        return sum(Model.X[i, j] for i in Model.Nodes) == 1
    else:
        return Constraint.Skip


Model.destination = Constraint(Model.Nodes, rule=destination_restriction)


# Restricción nodo intermedio
def intermediate_restriction(Model, i):
    if i != 1 and i != 5:
        return sum(Model.X[i, j] for j in Model.Nodes) - sum(Model.X[j, i] for j in Model.Nodes) == 0
    else:
        return Constraint.Skip


Model.intermediate = Constraint(Model.Nodes, rule=intermediate_restriction)

f1_const = 5
f1_vec = []
f2_vec = []

while f1_const >= 2:

    def f1_constraint(Model):
        return Model.f1 <= f1_const

    Model.f1_constraint = Constraint(rule=f1_constraint)

    SolverFactory('glpk').solve(Model)
    f1_vec.append(value(Model.f1))
    f2_vec.append(value(Model.f2))
    f1_const -= 1
    delete_component(Model, 'f1_constraint')

plt.plot(f1_vec, f2_vec, 'o-.')
plt.title('Frente óptimo de Pareto')
plt.xlabel('F1')
plt.ylabel('F2')

plt.grid(True)
plt.show()
