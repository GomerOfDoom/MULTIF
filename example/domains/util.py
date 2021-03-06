from __future__ import division
import numpy as np
from scipy.optimize import linprog as sp_linprog

# checking to see if system has gurobi installed
try:
	HAS_GUROBI = True
	import gurobipy as gpy
except ImportError, e:
	HAS_GUROBI = False
	pass

def clencurt(n, a = -1, b = 1):
	""" Return the Clenshaw-Curtis quadtrature nodes and weights on [a,b]

	Modified from Trefethen's clencurt.m code and Embree's clencurtab.m code
	"""

	theta = np.pi*np.arange(0,n+1)/n
	x = np.cos(theta)
	w = np.zeros(n+1)
	v = np.ones(n-1)
	if n % 2 == 0:
		w[0] = 1/(n**2 - 1)
		w[n] = w[0]
		for k in range(1, n//2):
			v -= 2 * np.cos( 2 * k * theta[1:n] ) / (4 * k**2 - 1)
		v -= np.cos(n * theta[1:n])/(n**2 - 1)
	else:
		w[0] = 1/n**2
		w[n] = w[0]
		for k in range(1, (n-1)//2 + 1):
			v -= 2 * np.cos( 2 * k * theta[1:n] )/ (4 * k**2 - 1)
	
	w[1:n] = 2*v/n
	
	x = a + (b - a)/2 * (1 + x)
	w = (b - a)/2 * w
	return x, w

def gauss_hermite(n):
	return np.polynomial.hermite.hermgauss(n)



def gurobi_linear_program(c, A_ub = None, b_ub = None, lb = None, ub = None, A_eq = None, b_eq = None):
	model = gpy.Model()
	model.setParam('OutputFlag', 0)
	model.setParam('NumericFocus', 3)	# improve handeling of numerical instabilities
	
	n = c.shape[0]	

	# Add variables to model
	vars_ = []
	if lb is None:
		lb = -np.inf * np.ones(n)
	if ub is None:
		ub = np.inf * np.ones(n)

	for j in range(n):
		if np.isfinite(lb[j]):
			lb_ = lb[j]
		else:
			lb_ = -gpy.GRB.INFINITY

		if np.isfinite(ub[j]):
			ub_ = ub[j]
		else:
			ub_ = gpy.GRB.INFINITY
		vars_.append(model.addVar(lb=lb_, ub=ub_, vtype=gpy.GRB.CONTINUOUS))

	model.update()

	# Populate linear constraints
	if A_ub is not None and A_ub.shape[0] > 0:
		for i in range(A_ub.shape[0]):
			expr = gpy.LinExpr()
			for j in range(n):
				expr += A_ub[i,j]*vars_[j]
			model.addConstr(expr, gpy.GRB.LESS_EQUAL, b_ub[i])
	
	# Add inequality constraints
	if A_eq is not None and A_eq.shape[0] > 0:
		m_eq, n_eq = A_eq.shape
		for i in range(m_eq):
			expr = gpy.LinExpr()
			for j in range(n_eq):
				expr += A_eq[i,j]*vars_[j]
			model.addConstr(expr, gpy.GRB.EQUAL, b_eq[i])

	# Populate objective
	obj = gpy.LinExpr()
	for j in range(n):
		obj += c[j]*vars_[j]
	model.setObjective(obj)
	model.update()

	# Solve
	model.optimize()

	if model.status == gpy.GRB.OPTIMAL:
		return np.array(model.getAttr('x', vars_)).reshape((n,))
	else:
		raise Exception('Gurobi did not solve the LP. Blame Gurobi.')

def linprog(c, A_ub = None, b_ub = None, A_eq = None, b_eq = None,  lb = None, ub = None, **kwargs):
	if HAS_GUROBI:
		return gurobi_linear_program(c, A_ub, b_ub, lb = lb, ub = ub, A_eq = A_eq, b_eq = b_eq)
	else:
		if lb is not None and ub is not None:
			bounds = [(lb_, ub_) for lb_, ub_ in zip(lb, ub)]
		elif ub is not None:
			bounds = [(None, ub_) for ub_ in ub]
		elif lb is not None:
			bounds = [(lb_, None) for lb_ in lb]
		else:
			bounds = None
		res = sp_linprog(c, A_ub = A_ub, b_ub = b_ub, A_eq = A_eq, b_eq = b_eq, bounds = bounds, **kwargs)
		if res.success:
			return res.x
		else:
			raise Exception("Could not find feasible starting point: " + res.message)


def find_feasible_boundary(p, v, eps, alphaleft, alpharight, A, b):
    
    # Find ends of feasible range
    err = eps*2.;
    count = 0;
    # First, bracket the boundary
    while(1):
        xtmp = p + alpharight*v;
        err = np.max(A.dot(xtmp)-np.squeeze(b));
        if( err < 0. ):
            alpharight = alpharight*2.;
        else:
            break;
        if( count > 100 ):
            print('Maximum number of iterations reached for bracketing.');
            break;
        count = count + 1;
    # Next, perform bisection until boundary is within tolerance eps    
    count = 0;
    while(np.abs(err) > eps):
        alpha = (alphaleft + alpharight)/2.;
        xtmp = p + alpha*v;
        err = np.max(A.dot(xtmp)-np.squeeze(b));
        if( err < 0. ):
            alphaleft = alpha;
        else:
            alpharight = alpha;
        if( count > 100 ):
            print('Maximum number of iterations reached for bisection.');
            break;
        count = count + 1;
        
    return p + alpha*v/2.;