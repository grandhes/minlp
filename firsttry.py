import time
from gurobipy import GRB, Model
## Sample data

supplier_risk = {'supplier1': 10, 'supplier2': 1000, 'supplier3': 10,'supplier4': 1000, 'supplier5': 19, 'supplier5': 20 }

Product_matrix = {
    ('supplier1','product1'): 1,
    ('supplier1','product2'): 100,
    ('supplier1','product3'): 1,
    ('supplier1','product11'): 100,
    ('supplier1','product12'): 100,
    ('supplier1','product13'): 100,    

    ('supplier2','product1'): 1,
    ('supplier2','product2'): 1,
    ('supplier2','product3'): 1,
    ('supplier2','product11'): 100,
    ('supplier2','product12'): 100,
    ('supplier2','product13'): 100,  

    ('supplier3','product1'): 1,
    ('supplier3','product2'): 1,
    ('supplier3','product3'): 100,
    ('supplier3','product11'): 100,
    ('supplier3','product12'): 100,
    ('supplier3','product13'): 100,  

    ('supplier4','product1'): 100,
    ('supplier4','product2'): 100,
    ('supplier4','product3'): 100,
    ('supplier4','product11'): 1,
    ('supplier4','product12'): 1,
    ('supplier4','product13'): 100,  

    ('supplier5','product1'): 100,
    ('supplier5','product2'): 100,
    ('supplier5','product3'): 100,
    ('supplier5','product11'): 1,
    ('supplier5','product12'): 1,
    ('supplier5','product13'): 1,  

    ('supplier6','product1'): 100,
    ('supplier6','product2'): 100,
    ('supplier6','product3'): 100,
    ('supplier6','product11'): 1,
    ('supplier6','product12'): 100,
    ('supplier6','product13'): 1        

}

suppliers = ['supplier1','supplier2', 'supplier3', 'supplier4', 'supplier5', 'supplier6']
products = ['product1','product2', 'product3', 'product11', 'product12', 'product13']

# Declare and initialize model
m = Model('BOM_Suppliers')

# Create decision variables for the supplier model
x = m.addVars(Product_matrix.keys(),
                  vtype=GRB.INTEGER,
                  name="x")

y = m.addVars(supplier_risk.keys(),
                  vtype=GRB.BINARY,
                  name="y")

## create constraint
product_constraints = m.addConstrs((x.sum('*',p) == 1 for p in products ), name='product_constraints')
# constraint for supplier 1
supplier_constraints = m.addConstrs( (x.sum(s,'*') - y.sum(s) * 1000 <= 0 for s in suppliers ), name='supplier_constraints')

## set objective
m.setObjective(x.prod(Product_matrix) + y.prod(supplier_risk), GRB.MINIMIZE)

# Save model for inspection
    
m.write('BOM_Suppliers.lp')

m.optimize()

print(time.ctime())
if m.status == GRB.OPTIMAL:
    print(f'Optimal cost: {m.objVal}')
else:
    print("Not solved to optimality. Optimization status:", m.status)


for v in m.getVars():
    if v.x > 1e-6:
        print(v.varName, v.x)