from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, LpStatus, lpSum, value, apis

# 1. Initialise model
model = LpProblem("Maximize LP", LpMaximize)

# 2. Define Decision Variables:
x1 = LpVariable('X1', lowBound=0, upBound=None, cat="Continuous")
x2 = LpVariable('X2', lowBound=0, upBound=None, cat="Continuous")
x3 = LpVariable('X3', lowBound=0, upBound=None, cat="Continuous")

# 3. Define objective function:
model += lpSum(1 * x1 + 4 * x2 + 2 * x3), 'obj'

# 4. Define constraints: our model's limitations
model += lpSum(5 * x1 + 2 * x2 + 2 * x3) <= 145, 'c1'
model += lpSum(4 * x1 + 8 * x2 - 8 * x3) <= 260, 'c2'
model += lpSum(1 * x1 + 1 * x2 + 4 * x3) <= 190, 'c3'

# 5. Solve model
model.solve(apis.PULP_CBC_CMD(msg=0))

# 6. Check feasibility of Q = (0, 52.5, 20)
Q = [0, 52.5, 20]
feasibility = [
    5 * Q[0] + 2 * Q[1] + 2 * Q[2] <= 145,
    4 * Q[0] + 8 * Q[1] - 8 * Q[2] <= 260,
    Q[0] + Q[1] + 4 * Q[2] <= 190
]
is_feasible = all(feasibility)

# 7. Initialise the dual model
dual_model = LpProblem("Minimize Dual LP", LpMinimize)

# 8. Define Decision Variables for the dual problem
y1 = LpVariable('Y1', lowBound=0, upBound=None, cat="Continuous")
y2 = LpVariable('Y2', lowBound=0, upBound=None, cat="Continuous")
y3 = LpVariable('Y3', lowBound=0, upBound=None, cat="Continuous")

# 9. Define Objective Function for the dual problem
dual_model += lpSum(145 * y1 + 260 * y2 + 190 * y3), 'Dual_Objective'

# 10. Define Constraints for the dual problem
dual_model += lpSum(5 * y1 + 4 * y2 + 1 * y3) >= 1, 'Dual_Constraint1'
dual_model += lpSum(2 * y1 + 8 * y2 + 1 * y3) >= 4, 'Dual_Constraint2'
dual_model += lpSum(2 * y1 - 8 * y2 + 4 * y3) >= 2, 'Dual_Constraint3'

# 11. Solve the dual problem
dual_model.solve(apis.PULP_CBC_CMD(msg=0))

# 12. Complementary Slackness Check
primal_slack = [c.slack for c in model.constraints.values()]
dual_slack = [c.slack for c in dual_model.constraints.values()]
primal_vars = [value(v) for v in model.variables()]
dual_vars = [value(v) for v in dual_model.variables()]

# Check Complementary Slackness for Primal
CS_primal = [s == 0 for s, var in zip(dual_slack, primal_vars) if var > 0]

# Check Complementary Slackness for Dual
CS_dual = [s == 0 for s, var in zip(primal_slack, dual_vars) if var > 0]

print(f"____Primal Solution____")
print(f"Status: {LpStatus[model.status]}")
for name, c in model.constraints.items():
    print(f"{name}: slack = {c.slack:.2f}, shadow price = {c.pi:.2f}")

for v in model.variables():
    print(v.name,"=", v.varValue)
print("Objective = ", value(model.objective))

print(f"Feasibility of Q = {Q}: {'Feasible' if is_feasible else 'Not Feasible'}")

print(f"\n____Dual Solution____")
print(f"Status: {LpStatus[dual_model.status]}")
for name, c in dual_model.constraints.items():
    print(f"{name}: slack = {c.slack:.2f}, shadow price = {c.pi:.2f}")
for v in dual_model.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Objective(Dual) = {value(dual_model.objective)}\n")

# Check Complementary Slackness
print('____CS verification____')
print(f"Complementary Slackness Satisfied (Primal): {all(CS_primal)}")
print(f"Complementary Slackness Satisfied (Dual): {all(CS_dual)}")

print(f"Q = {Q} {'is the solution' if all(CS_dual) and all(CS_primal) else 'is not the solution'}")


