# kth1.py
# 
# simple MPEC # 2

import coopr.environ
from coopr.pyomo import *
from coopr.mpec import *


model = ConcreteModel()

model.z1 = Var(within=NonNegativeReals, initialize=0)
model.z2 = Var(within=NonNegativeReals, initialize=1)

model.objf = Objective(expr=model.z1 + (model.z2 - 1)**2)

model.compl = Complementarity(expr=0 <= model.z1, model.z2 >= 0)


