#!/usr/bin/env python3
''' 
Cheatsheet of basic SciPy functionality 

References:
    https://docs.scipy.org/doc/scipy/reference/index.html
'''

import numpy as np
import numpy.testing as test
################################################################################
# Constants
from scipy import constants
print('== Constants ==')
print('Pi =', constants.pi)
print('c =', constants.c,'=',constants.speed_of_light)
for c in constants.find('vacuum'):
    val, unit, err = constants.physical_constants[c]
    assert val == constants.value(c)
    assert unit == constants.unit(c)
    prec = constants.precision(c)
    assert prec == err/val
    print(f'{c:30} = {val:20} +/- {err:8} {unit}')
print('SI prefixes : ',constants.zepto,'to',constants.yotta)
print('Convert to SI : 2 years, 6 weeks, and 4 days = ', 2*constants.year + 6*constants.week + 4*constants.day,'sec')
print()

################################################################################
# Statistical functions
from scipy import stats
print('== Continuous RV ==')
rv = stats.norm(loc=10, scale=2)
arr = rv.rvs(size=6, random_state=0)
print('Mean :', rv.mean(),'; Std Dev =', rv.std(),'; Var =', rv.var())
print('Sampled array :', arr)
print('CDF value :', rv.cdf(arr))
test.assert_allclose(arr, rv.ppf(rv.cdf(arr)))
print('PDF value :', rv.pdf(arr))
arr = rv.rvs(size=150, random_state=0)
mean, std_dev = stats.norm.fit(arr)
print(f'Fitted mean and std dev : {mean:.2f} +/- {std_dev:.2f}')
print()

print('== Discrete RV ==')
rv = stats.binom(n=20, p=0.5)
arr = rv.rvs(size=6, random_state=0)
print('Mean :', rv.mean(),'; Std Dev =', rv.std(),'; Var =', rv.var())
print('Sampled array :', arr)
print('CDF value :', rv.cdf(arr))
test.assert_allclose(arr, rv.ppf(rv.cdf(arr)))
print('PDF value :', rv.pmf(arr))
print()


################################################################################
# Special functions
from scipy import special
print("Special functions")
print("Error function :", special.erf([1,0.5,0,0.5,1]))
print()

################################################################################
# Integration and ODEs
from scipy import integrate
print("== Numerical integration of functions ==")
func = lambda x,y,z : x*y*z
y = 2
z = 1
x0, x1 = -1, 2
y0, y1 = lambda x : -1, lambda x : 2
z0, z1 = lambda x, y : -1, lambda x, y : 2
(result_1d, err_1d) = integrate.quad(func, x0, x1, args = (y,z))
(result_2d, err_2d) = integrate.dblquad(func, x0, x1, y0, y1, args = (z,))
(result_3d, err_3d) = integrate.tplquad(func, x0, x1, y0, y1, z0, z1)
print(f"1D Integral : {result_1d:.3f} +/- {err_1d}")
print(f"2D Integral : {result_2d:.3f} +/- {err_2d}")
print(f"3D Integral : {result_3d:.3f} +/- {err_3d}")
print()

print("== Numerical integration of samples ==")
x_arr = np.linspace(x0, x1, 10)
result_1d = integrate.simps(func(x_arr,y,z), x_arr)
print(f"1D Integral : {result_1d:.3f}")
print()

#print("== Numerical integration of ODEs ==")

################################################################################
# Interpolation
from scipy import interpolate
print('== 1D Interpolation ==')
x1 = np.linspace(0,10,11)
y1 = np.cos(x1)
x2 = np.linspace(0,10,101)
y2 = np.cos(x2)
for kind in ['previous', 'next', 'nearest', 'linear', 'cubic']:
    f = interpolate.interp1d(x1,y1, kind=kind)
    y2_interp = f(x2)
    resid = y2-y2_interp
    mean = np.mean(resid)
    std = np.std(resid)
    print(f"{kind:>10} residual : {mean:.4f} +/- {std:.4f}")
print()

#print('== 1D Spline Interpolation ==')

################################################################################
# Linear algebra (scipy.linalg)
# pretty straightforward. use as needed

################################################################################
# Optimization and root finding (scipy.optimize)
from scipy import optimize
print("== Univariate optimizers ==")
## Unconstrained
f = lambda x : x**2 - 30*2**(-(x-5)**2) # parabola with hidden global minima at x=5
res1A = optimize.minimize_scalar(f, method='brent') # Brent is default
res1B = optimize.minimize_scalar(f,(2,6))
res2A = optimize.minimize_scalar(f,(4,6))
res2B = optimize.minimize_scalar(f,(3,4,8))
assert int(res1A.x) == int(res1B.x)
assert int(res2A.x) == int(res2B.x)
assert int(res1A.x) != int(res2A.x)
## Bounded
res1C = optimize.minimize_scalar(f, bounds=(-1,10), method='bounded')
res2C = optimize.minimize_scalar(f, bounds=(1,10), method='bounded')
assert int(res1C.x) == int(res1A.x)
assert int(res2C.x) == int(res2A.x)
print(f'Brent fit ( local min) : min(f) = f({res1A.x:.2f}) = {res1A.fun:.2e}; [nit,fev] = [{res1A.nit},{res1A.nfev}]')
print(f'Brent fit (global min) : min(f) = f({res2A.x:.2f}) = {res2A.fun:.2e}; [nit,fev] = [{res2A.nit},{res2A.nfev}]')
print(f'Bound fit ( local min) : min(f) = f({res1C.x:.2f}) = {res1C.fun:.2e}; [fev] = [{res1C.nfev}]')
print(f'Bound fit (global min) : min(f) = f({res2C.x:.2f}) = {res2C.fun:.2e}; [fev] = [{res2C.nfev}]')

print()

print("== Multivariate optimizers ==")
func  = lambda x,y,z : x**2 + (y-1)**2 + (z+1)**2 # min at [0,1,-1]
jac   = lambda x,y,z : np.array([2*x, 2*(y-1), 2*(z+1)])
hess  = lambda x,y,z : np.array([[2, 0, 0],
                                 [0, 2, 0],
                                 [0, 0, 2]])
hessp = lambda x,y,z,px,py,pz : np.array( [2*px, 2*py, 2*pz] )
x0 = np.array([0,0,0])

func_wrap  = lambda x   : func( x[0],x[1],x[2])
jac_wrap   = lambda x   : jac(  x[0],x[1],x[2])
hess_wrap  = lambda x   : hess( x[0],x[1],x[2])
hessp_wrap = lambda x,p : hessp(x[0],x[1],x[2], p[0], p[1], p[2])

# bound constraints
lb = [-5, -5, -5]
ub = [ 5,  5,  5]
bounds = optimize.Bounds(lb, ub)
# Constraints for trust_constr
## linear constraints
### constraint 1 ) -5 <  x + y + z < 5
### constraint 2 ) -5 < -x - y - z < 5
### constraint 3 ) -5 < 2x + 3y + 4z < 5
cons = [
    [ 1,  1,  1],
    [-1, -1, -1],
    [ 2,  3,  4],
    ]
lb = [-5, -5, -5]
ub = [ 5,  5,  5]
lin_constraints = optimize.LinearConstraint(cons, lb, ub)
## non-linear constraints
### constraint 1 ) -5 <  xyz < 5
### constraint 2 ) -5 < -xyz < 5
### constraint 3 ) 0 < x^2 + y^2 + z^2 < 5
def cons_f(x):
    x,y,z = x[0],x[1],x[2]
    cons1 = x*y*z
    cons2 = -x*y*z
    cons3 = x**2 + y**2 + z**2
    return [cons1, cons2, cons3]
lb = [-5,-5, 0]
ub = [ 5, 5, 5]
def cons_jac(x):
    x,y,z = x[0],x[1],x[2]
    # gradients  dx  , dy  , dz
    jac_cons1 = [y*z,  x*z,  x*y ]
    jac_cons2 = [-y*z, -x*z, -x*y]
    jac_cons3 = [2*x,  2*y,  2*z ]
    return [jac_cons1, jac_cons2, jac_cons3]
def cons_hessp(x,p):
    x,y,z = x[0],x[1],x[2]
    # double gradient       dx dy dz
    hess_cons1 = np.array([[0, z, y],  # dx
                           [z, 0, x],  # dy
                           [y, x, 0]]) # dz
    #                       dx  dy  dz
    hess_cons2 = np.array([[ 0, -z, -y],  # dx
                           [-z,  0, -x],  # dy
                           [-y, -x,  0]]) # dz
    #                       dx dy dz
    hess_cons3 = np.array([[2, 0, 0],  # dx
                           [0, 2, 0],  # dy
                           [0, 0, 2]]) # dz

    return p[0]*hess_cons1 + p[1]*hess_cons2 + p[2]*hess_cons3

nonlin_constraints = optimize.NonlinearConstraint(cons_f, lb, ub, jac=cons_jac, hess=cons_hessp)

constraints_trust = [lin_constraints, nonlin_constraints]

# Constraints for SLSQP and COBYLA
def ineq_fun(x):
    # Same constraints as for trust_constr but changed to c(x) >= 0 form
    x,y,z = x[0],x[1],x[2]
    ineq1 = x*y*z + 5
    ineq2 = -x*y*z + 5
    ineq3 = 5 - (x**2 + y**2 + z**2)
    return np.array([ineq1, ineq2, ineq3])
def ineq_jac(x):
    x,y,z = x[0],x[1],x[2]
    #        dx    dy    dz
    ineq1 = [y*z,  x*z,  z*y]
    ineq2 = [-y*z, -x*z, -z*y]
    ineq3 = [2*x,  2*y,  2*z]
    return np.array([ineq1, ineq2, ineq3])
def eq_fun(x):
    # constraint 1) x**2 + y + z = 0
    x,y,z = x[0],x[1],x[2]
    eq1 = x**2 + y + z
    return np.array([eq1])
def eq_jac(x):
    x,y,z = x[0],x[1],x[2]
    eq1 = [2*x, 1, 1]
    return np.array([eq1])

ineq_constraints = {
    'type' : 'ineq',
    'fun'  : ineq_fun,
    'jac'  : ineq_jac,
}
eq_constraints = {
    'type' : 'eq',
    'fun'  : eq_fun,
    'jac'  : eq_jac,
}
constraints_slsqp = [eq_constraints, ineq_constraints]
constraints_cobyla = ineq_constraints

# Implementation (optimize.minimize)
methods = {
        # Method        : [  Jac,       Hess,       Hessp,      Constraints ]
        'Default'       : ['Optional', 'Unused',   'Unused',   'Unused'], # BFGS
        'Nelder-Mead'   : ['Unused',   'Unused',   'Unused',   'Unused'],
        'Powell'        : ['Unused',   'Unused',   'Unused',   'Unused'],
        'COBYLA'        : ['Unused',   'Unused',   'Unused',   'Optional'],
        'CG'            : ['Optional', 'Unused',   'Unused',   'Unused'],
        'BFGS'          : ['Optional', 'Unused',   'Unused',   'Unused'],
        'L-BFGS-B'      : ['Optional', 'Unused',   'Unused',   'Unused'],
        'TNC'           : ['Optional', 'Unused',   'Unused',   'Unused'], 
        'SLSQP'         : ['Optional', 'Unused',   'Unused',   'Optional'], 
        'trust-constr'  : ['Optional', 'Optional', 'Optional', 'Optional'],
        'Newton-CG'     : ['Required', 'Optional', 'Optional', 'Unused'],
        'dogleg'        : ['Required', 'Required', 'Unused',   'Unused'],
        'trust-exact'   : ['Required', 'Required', 'Unused',   'Unused'],
        'trust-ncg'     : ['Required', 'Required', 'Required', 'Unused'],
        'trust-krylov'  : ['Required', 'Required', 'Required', 'Unused'],
}

def eval_count_str(opt_res):
    evals = {k : f'{v}' for k,v in opt_res.items() if k.startswith('n') and k.endswith('ev')}
    eval_str = '[' + ','.join(evals.keys()) + '] = [' + ','.join(evals.values()) + ']'
    return eval_str

def print_result(m, res, fit_type=' '):
    x,y,z = np.round(res.x,3)
    nfev = res.nfev
    njev = res.njev if hasattr(res,'njev') else '-'
    nhev = res.nhev if hasattr(res,'nhev') else '-'
    nit  = res.nit  if hasattr(res,'nit') else '-'
    print(f'{m:12} fit {fit_type:>7} : [x,y,z]=[{x:4},{y:4},{z:4}]; [nit,fev,jev,hev] = [{nit:3},{nfev:3},{njev:3},{nhev:3}]')

for m, flags in methods.items():
    jac_op, hess_op, hessp_op, constrained = flags
    
    if m == 'Default': 
        res = optimize.minimize(func_wrap, x0)
        print_result(m, res)
        res = optimize.minimize(func_wrap, x0, jac=jac_wrap)
        print_result(m, res, '(Jac)')
        continue
    if jac_op == 'Unused' or jac_op == 'Optional':
        res = optimize.minimize(func_wrap, x0, method=m)
        print_result(m, res)
    if jac_op == 'Optional' or hess_op == 'Optional': 
        res = optimize.minimize(func_wrap, x0, method=m, jac=jac_wrap)
        print_result(m, res, '(Jac)')
    if hess_op == 'Optional' or hess_op == 'Required':
        res = optimize.minimize(func_wrap, x0, method=m, jac=jac_wrap, hess=hess_wrap)
        print_result(m, res, '(Hess)')
    if hessp_op == 'Optional' or hessp_op == 'Required':
        res = optimize.minimize(func_wrap, x0, method=m, jac=jac_wrap, hessp=hessp_wrap)
        print_result(m, res, '(Hessp)')
    
    if constrained == 'Optional':
        if m == 'trust-constr':
            cons = constraints_trust
            bds = bounds
        elif m == 'SLSQP':
            cons = constraints_slsqp
            bds = bounds
        elif m == 'COBYLA':
            cons = constraints_cobyla
            bds = None
        
        res = optimize.minimize(func_wrap, x0, method=m, constraints=cons, bounds=bds)
        #res = optimize.minimize(func_wrap, x0, method=m, constraints=cons)
        print_result(m, res, '(Const)')
    

print()

# Least squares

# Global minimization
print("== Global minimization ==")
f = lambda x : x**2 - 2*np.cos(5*x)
bounds = [(-5,5)]
results = {}
results['shgo'] = optimize.shgo(f, bounds)
results['dual_annealing'] = optimize.dual_annealing(f, bounds)
results['differential_evolution'] = optimize.differential_evolution(f, bounds)
#results['basinhopping'] = optimize.basinhopping(f,bounds)
buff = len(max(results.keys(),key=len)) + 1
for m, res in results.items():
    eval_str = eval_count_str(res) 
    print(f'{m:>{buff}} : Global min at {res.x[0]: .2f}; {eval_str}')
print()

# Roots
## root finding methods
print("== Root finding ==")
f   = lambda x : 5*(x)*(x+1)*(x-1) # = 5*(x**3) - x
jac = lambda x : 15*(x**2) - 1
guess = 0.3
methods = {
        # Method   :  Jacobian
        'hybr'     : 'Optional',
        'lm'       : 'Optional',
        'broyden1' : 'Unused',
        'broyden2' : 'Unused',
        'anderson' : 'Unused',
        'krylov'   : 'Unused',
        'df-sane'  : 'Unused',
}
for m, flag in methods.items():
    res = optimize.root(f, x0=guess, method=m)
    x = res.x[0] if res.x.ndim > 0 else res.x
    fun = res.fun[0] if res.fun.ndim > 0 else res.fun
    assert np.allclose(f(x), fun)
    keys = ', '.join(sorted(res.keys()))
    print(f'{m:>10}       : x0 = {guess:+} -> root @ f({x:+.2f}) (keys = {keys})')
    if flag == 'Optional':
        res = optimize.root(f, jac=jac, x0=guess, method=m)
        print(f'{m:>10} (Jac) : x0 = {guess:+} -> root @ f({x:+.2f})')

print()

print("== Solving sets of equations ==")
def f(args):
    x, y = args[0], args[1]
    eq1 = y - np.sin(x)  # y = sin(x)
    eq2 = y - x          # y = x
    return np.array([eq1, eq2])
def jac(args):
    x, y = args[0], args[1]
    eq1_dx = np.cos(x)
    eq1_dy = np.sin(x)
    eq2_dx = -1
    eq2_dy = 1
    return np.array([
        [eq1_dx, eq1_dy],
        [eq2_dx, eq2_dy],
        ])
guess = [1,1]

res = optimize.root(f, x0=guess, jac=jac, method='hybr')
assert np.allclose(f(res.x), res.fun)
x, y = res.x[0], res.x[1]
print(f'x0 = [{guess[0]:+},{guess[1]:+}] -> root @ f({x=:+.2f},{y=:+.2f}) (keys = {keys})')
print()

################################################################################
# Clustering package (scipy.cluster)

################################################################################
# OTHER
# Input and output (import scipy.io as spio)
# Discrete Fourier transforms (scipy.fft)
# Legacy discrete Fourier transforms (scipy.fftpack)
# Signal processing (scipy.signal)
# Sparse matrices (scipy.sparse)
# Sparse linear algebra (scipy.sparse.linalg)
# Compressed sparse graph routines (scipy.sparse.csgraph)
# Spatial algorithms and data structures (scipy.spatial)
# Miscellaneous routines (scipy.misc)
